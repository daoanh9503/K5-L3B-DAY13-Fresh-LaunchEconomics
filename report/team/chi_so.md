# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | 82,83% (994/1.200) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | 27,12% (48/177) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | 4,25% (51/1.200) |
| Dùng | Nhóm tự đề xuất: % yêu cầu đủ điều kiện của nhóm trợ lý được nhân viên mở bằng trợ lý | số `agent_suggestion_shown` theo `staff_id` thuộc nhóm trợ lý, chia số `refund_request_created` trong phạm vi giao cho nhóm đó | Không cần tính |
| An toàn | Nhóm tự đề xuất: % đơn hoàn sai tiền qua kiểm tra mẫu hằng tuần (bắt lỗi ngầm như ca 5, 12, 17) | số đơn có `so_tien_da_hoan` khác `so_tien_dung` trong `audit_sample_checked`, chia số đơn được kiểm tra (100 đơn/tuần) | Không cần tính |

Chỉ số trong đợt chạy thử là 82,83% (chính), 27,12% (dùng), 4,25% (an toàn). Đợt chạy thử không có nhóm đối chứng, nên các số này chỉ mô tả đợt chạy thử, không cho biết trợ lý có làm chỉ số thay đổi hay không.

## Danh sách event

Ít nhất sáu event, mỗi event có `trace_id` để nối với trace của agent.

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | App khách | request_id, loai, so_tien, depot, staff_id, arm, trace_id | Khi khách gửi yêu cầu |
| `agent_run_completed` | Agent | attempt, tokens_in, tokens_out, tool_calls, status, trace_id | Sau mỗi lần chạy, kể cả lần lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | staff_id, so_tien_de_xuat, trace_id | Khi gợi ý hiện cho nhân viên |
| `staff_review_decision` | Nhân viên | quyet_dinh (giu/sua/bo), phut_xem_lai đo thật, trace_id | Khi nhân viên bấm giữ, sửa hoặc bỏ |
| `staff_rework_completed` | Nhân viên | phut_lam_lai đo thật, ly_do, trace_id | Khi làm lại xong |
| `refund_ledger_write` | Dịch vụ sổ cái | idempotency_key, so_tien, ket_qua (ok/loi), trace_id | Khi ghi lệnh hoàn vào sổ cái |
| `handoff_to_staff` | Agent | reason (thieu_du_lieu, ngoai_pham_vi, het_lan_chay), tom_tat, trace_id | Khi chuyển cho nhân viên |
| `ticket_closed` | Hệ thống ticket | closed_at, trace_id | Khi yêu cầu đóng |
| `ticket_reopened` | Khách | reopened_at, reason, trace_id | Khi khách mở lại |
| `audit_sample_checked` | Kế toán | so_tien_da_hoan, so_tien_dung, phien_ban_bang_gia, trace_id | Hằng tuần, 100 đơn mẫu |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, ghi event dùng để tính. Chỉ số nào không tính được từ danh sách event thì chưa đo được.

- Chính: `refund_request_created` (thời điểm tạo) + `ticket_closed` (đóng trong 24 giờ) + `ticket_reopened` (không mở lại trong 7 ngày).
- Dùng (bỏ qua gợi ý): `staff_review_decision` với quyet_dinh là sua hoặc bo, chia tổng số `staff_review_decision`.
- An toàn (lỗi lọt đến khách): `ticket_reopened` trong 7 ngày sau `ticket_closed`, chia số `refund_request_created`.
- Dùng (tự đề xuất): `agent_suggestion_shown` chia `refund_request_created` của nhóm trợ lý (lọc theo arm, staff_id).
- An toàn (tự đề xuất): `audit_sample_checked`. Hoàn trùng (ca 20) đo thêm bằng hai `refund_ledger_write` cùng mã đơn.
- Chi phí mỗi việc thành công: `agent_run_completed` (token, tool) + `staff_review_decision` và `staff_rework_completed` (phút đo thật thay cho cột simulated) chia số yêu cầu đóng không mở lại.

## E2 · Rủi ro kinh tế

Ít nhất hai dòng, số lấy từ bảng độ nhạy (`bang_chi_phi.md`). Mọi số chi phí là simulated.

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | +51,8%, từ 4.472 đ lên 6.787 đ mỗi việc thành công [simulated] (B1) | Tỉ lệ làm lại theo tuần trong phạm vi > 7% (đợt chạy thử: 4,9%), từ `staff_rework_completed` | Thu hẹp về noi_dia, rà 20 trace làm lại gần nhất để tìm nguyên nhân | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài | 11.743 đ = 0,98× của 12.000 đ, hoặc 12.415 đ = 1,03× nếu làm lại 15,3 phút như dữ liệu [simulated] (B4); hoà vốn khi mỗi lần xem lại ≤ 5,1 phút | % yêu cầu được xem lại còn > 50% ở cuối bước rollout 0,25 (đợt chạy thử: 14,8%), từ `staff_review_decision` | Giảm xem lại theo bậc (100% → 50% → 20%) khi tỉ lệ sửa + bỏ < 15% trong 1 tuần | Trưởng nhóm CSKH |
| Khối lượng thấp hơn dự kiến | Chi phí cố định 40 triệu đ/tháng: +1.185 đ/việc ở 45.000 yêu cầu/tháng, +2.370 đ/việc nếu còn một nửa, tổng 5.784 đ = 0,48× [simulated] (A4) | Số việc thành công theo tuần < 50% kế hoạch | Không mở rộng pilot, đàm phán lại chi phí cố định | PM trợ lý hoàn phí |
