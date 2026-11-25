# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: (điền họ tên) · Người gắn nhãn 2: chưa có (làm một mình, đang hỏi coach cách xử lý)

Ghi chú trung thực: người gắn nhãn 1 tự chọn nhãn từng ca, có dùng Claude để đặt câu hỏi gợi ý theo bảng định nghĩa năm loại (không đưa đáp án). Ca 1, 5, 8 đổi nhãn sau câu hỏi gợi ý. Cột "Nhãn thống nhất" chốt sau khi so với nhãn tham khảo; chỉ ca 20 khác.

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | chưa có | — | Do người dùng |
| 2 | Hệ thống | chưa có | — | Hệ thống |
| 3 | Ngữ cảnh | chưa có | — | Ngữ cảnh |
| 4 | Giới hạn hệ thống | chưa có | — | Giới hạn hệ thống |
| 5 | Ngầm | chưa có | — | Ngầm |
| 6 | Do người dùng | chưa có | — | Do người dùng |
| 7 | Hệ thống | chưa có | — | Hệ thống |
| 8 | Hệ thống | chưa có | — | Hệ thống |
| 9 | Do người dùng | chưa có | — | Do người dùng |
| 10 | Ngữ cảnh | chưa có | — | Ngữ cảnh |
| 11 | Giới hạn hệ thống | chưa có | — | Giới hạn hệ thống |
| 12 | Ngầm | chưa có | — | Ngầm |
| 13 | Giới hạn hệ thống | chưa có | — | Giới hạn hệ thống |
| 14 | Do người dùng | chưa có | — | Do người dùng |
| 15 | Hệ thống | chưa có | — | Hệ thống |
| 16 | Ngữ cảnh | chưa có | — | Ngữ cảnh |
| 17 | Ngầm | chưa có | — | Ngầm |
| 18 | Ngữ cảnh | chưa có | — | Ngữ cảnh |
| 19 | Giới hạn hệ thống | chưa có | — | Giới hạn hệ thống |
| 20 | Ngầm | chưa có | — | Hệ thống |

**Tỉ lệ đồng thuận:** chưa tính được, chỉ có một bộ nhãn. Nhãn người 1 khớp nhãn tham khảo 19/20 = 95%.

Phân bố nhãn thống nhất: Do người dùng 4 (1, 6, 9, 14) · Hệ thống 5 (2, 7, 8, 15, 20) · Ngữ cảnh 4 (3, 10, 16, 18) · Giới hạn hệ thống 4 (4, 11, 13, 19) · Ngầm 3 (5, 12, 17).

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- Ca 20 (Ngầm → Hệ thống): thiếu khoá chống trùng là trợ lý làm sai thiết kế; hoàn hai lần lộ ra ngay ở sổ cái (hai lệnh cùng mã đơn), nên là Hệ thống. Ngầm chỉ dùng khi không có dấu vết nào lộ ra cho tới lúc kiểm tra mẫu (ca 5, 12, 17).
- Ca 8 (đổi khi gắn): trích dẫn sai nằm ngay trong câu trả lời, ai đọc cũng thấy, nên là Hệ thống, không phải Ngầm.
- Ca 1, 6, 9, 14: gốc lỗi là đầu vào hoặc thao tác của khách → Do người dùng; việc trợ lý nên kiểm tra hay gợi ý thêm ghi ở cột khắc phục.
- Ca 13: ngoài phạm vi thì là Giới hạn hệ thống, kể cả khi trợ lý xử lý giới hạn đó kém.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Event `bank_refund_rejected` với lý do sai số tài khoản, gắn `trace_id`; đếm theo ngày, cảnh báo khi quá 1% số lệnh hoàn | Kiểm tra độ dài và định dạng số tài khoản theo ngân hàng trước khi tạo lệnh; đọc lại 4 số cuối cho khách xác nhận | PM trợ lý hoàn phí |
| 20 | Hệ thống | Đối soát sổ cái mỗi giờ: hai lệnh hoàn cùng mã đơn trong 24 giờ; ngưỡng 0 ca | Thêm khoá chống trùng theo mã đơn cho mọi lệnh hoàn; khi khách gửi lại thì trả trạng thái lệnh đang xử lý thay vì tạo lệnh mới | Kỹ sư trưởng agent |
| 16 | Ngữ cảnh | Event `notification_sent` có giờ gửi; theo tuần, đếm tin gửi 22:00–07:00 và số phản ánh "làm phiền"; ngưỡng 0,5% số tin | Giữ tin không khẩn trong khung 22:00–07:00 và gửi lúc 07:00; chỉ gửi ngay khi khách bật nhận thông báo đêm | Trưởng nhóm CSKH |
| 13 | Giới hạn hệ thống | Event `out_of_scope_detected` với chủ đề (bảo hiểm, …), gắn `trace_id`; theo tuần, so với số câu trả lời chung chung bị khách hỏi lại | Khi nhận ra yêu cầu ngoài phạm vi, nói rõ "trợ lý không xử lý hoàn phí bảo hiểm" và chuyển kèm đầu mối của công ty bảo hiểm đối tác | PM trợ lý hoàn phí |
| 12 | Ngầm | Theo dõi tiền token mỗi yêu cầu theo depot, hằng ngày; cảnh báo khi một depot vượt 1,5 lần trung vị các depot trong 2 ngày liên tiếp | Kiểm tra schema đầu ra của tool, thiếu trường thì báo lỗi ngay thay vì gọi lại; ghi số lần gọi tool vào trace | Kỹ sư trưởng agent |
