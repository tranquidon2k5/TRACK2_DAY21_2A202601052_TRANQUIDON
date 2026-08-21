from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import storage
import joblib
import os

app = FastAPI()

ARTIFACT_BUCKET = os.environ.get("ARTIFACT_BUCKET", "dummy-bucket")
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """Tải file model.joblib từ cloud storage về máy khi server khởi động."""
    if os.path.exists(MODEL_PATH):
        print(f"Local model found at {MODEL_PATH}")
        return
    client = storage.Client()
    bucket = client.bucket(ARTIFACT_BUCKET)
    blob = bucket.blob(MODEL_KEY)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    blob.download_to_filename(MODEL_PATH)
    print(f"Downloaded model from gs://{ARTIFACT_BUCKET}/{MODEL_KEY} to {MODEL_PATH}")


try:
    download_model()
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"Warning loading model: {e}")
    if os.path.exists("models/model.joblib"):
        model = joblib.load("models/model.joblib")
    else:
        model = None


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    """Endpoint kiểm tra sức khỏe server."""
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    """
    Endpoint suy luận.

    Đầu vào: JSON {"features": [f1, f2, ..., f10]}
    Đầu ra:  JSON {"prediction": <0|1>, "label": <"thu_nhap_thap"|"thu_nhap_cao">}
    """
    if len(req.features) != 10:
        raise HTTPException(status_code=400, detail="Expected 10 features (adult income)")

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    preds = model.predict([req.features])
    pred = int(preds[0])
    label = "thu_nhap_cao" if pred == 1 else "thu_nhap_thap"
    return {"prediction": pred, "label": label}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
