# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Trần Quí Đôn |
| MSSV | 2A202601052 |
| Lớp / Khóa | K4 |
| Repo GitHub |https://github.com/tranquidon2k5/TRACK2_DAY21_2A202601052_TRANQUIDON|
| Ngày nộp | 21/08/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |
| 4 | 150 | 0.15 | 4 | 0.7182 | 0.8760 |

**Bộ siêu tham số đã chọn:** `n_estimators=150`, `learning_rate=0.15`, `max_depth=4`.

**Lý do:** Bộ siêu tham số này đạt điểm F1 cao nhất (0.7182) trên tập holdout, vượt qua ngưỡng 0.65. Mặc dù Lần chạy 1 có accuracy nhỉnh hơn một chút (0.8780 vs 0.8760), Lần 4 phân loại lớp thu nhập cao tốt hơn hẳn. Tăng max_depth lên 4 và learning_rate lên 0.15 giúp mô hình nâng cao hiệu quả dự đoán mà không gây quá khớp.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Census Income mất cân bằng lớp khi chỉ 24.8% mẫu thuộc lớp thu nhập cao (>50K). Một mô hình vô dụng luôn đoán "thu nhập thấp" vẫn đạt accuracy 0.752 nhưng F1 bằng 0. Do đó accuracy tạo cảm giác chính xác giả tạo. F1-score đo lường sự cân bằng giữa Precision và Recall trên lớp dương. Không dùng `average="weighted"` hay `"macro"` vì chúng bị ảnh hưởng lớn bởi lớp đa số.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| GitHub Actions thất bại khi pull dữ liệu DVC | Runner trên CI thiếu AWS credentials và thư viện `boto3`. | Thêm GitHub Secrets cho AWS credentials và cập nhật workflow cài bổ sung `boto3`. |
| Cập nhật DVC remote gặp lỗi kết nối S3 | Cấu hình endpoint S3 trong `.dvc/config` chưa đồng bộ với môi trường. | Điều chỉnh cấu hình DVC remote S3 và nạp biến môi trường xác thực đầy đủ. |

---

## 4. So Sánh Bước 2 và Bước 3 (bắt buộc, 2 - 3 câu)

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7182 | 0.8760 |
| Bước 3 (thêm `train_batch2`) | 0.7297 | 0.8800 |

**Nhận xét:** Khi bổ sung thêm 22.361 mẫu dữ liệu từ `train_batch2`, F1-score tăng nhẹ từ 0.7182 lên 0.7297 và Accuracy tăng từ 0.8760 lên 0.8800. Do dữ liệu mới được trích xuất ngẫu nhiên từ cùng một phân phối với tập huấn luyện ban đầu, việc tăng gấp đôi dung lượng dữ liệu giúp mô hình học thêm được một số đặc trưng biên nhưng không tạo ra sự thay đổi đột biến. Quan trọng nhất, quy trình CI/CD đã tự động kích hoạt huấn luyện lại và kiểm tra chất lượng thành công ngay sau khi commit con trỏ DVC mà không cần thao tác thủ công.
