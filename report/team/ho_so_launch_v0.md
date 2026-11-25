# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: Fresh · Lớp: L3B

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | 4.472 đ [simulated], gấp 16,3 lần hoá đơn token + tool chia số yêu cầu (274,7 đ); giờ nhân viên chiếm 92,5% (`bang_chi_phi.md` A2) | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | 1. số ca làm lại ±51,8% · 2. tỉ lệ xem lại ±40,7% · 3. lương nhân viên +23,1%; giá token chỉ ±5,6% [simulated] (B1) | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Phạm vi noi_dia + hang_nang: 4.599 đ = 0,38× của 12.000 đ đã cộng cố định ở 45.000 yêu cầu/tháng; cả hệ thống toàn mẫu 5.865 đ = 0,49×; quoc_te 1,88× nên loại [simulated] (A3, A4) | Giả lập | Giám đốc vận hành LogiX-VN |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Trong đợt chạy thử: chính 82,83% · bỏ qua gợi ý 27,12% · mở lại 7 ngày 4,25%; 10 event có trace_id (`chi_so.md`) | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 5 · Bảng lỗi và cách khắc phục | 20 ca: 4 người dùng · 5 hệ thống · 4 ngữ cảnh · 4 giới hạn · 3 ngầm; một bộ nhãn, khớp tham khảo 19/20; 5 dòng khắc phục có ngưỡng đo được (`bang_loi.md`) | Xong, có bằng chứng | Kỹ sư trưởng agent |
| 6 · Pilot plan | Chia theo nhân viên 20 + 20, ngẫu nhiên; mde 6 điểm cần 859 hiệu dụng mỗi nhóm (≥ 299 yêu cầu/người); power chỉ 0,64 nếu tác động thật là 5 điểm; 3 luật dừng; quyết định 2027-01-15 (`pilot_plan.yaml`) | Xong, có bằng chứng | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | Làm lại ×2: 6.787 đ (+51,8%); xem lại 100%: 11.743 đ = 0,98× (1,03× nếu làm lại 15,3 phút); khối lượng còn một nửa: 5.784 đ = 0,48× [simulated] (`chi_so.md` E2) | Giả lập | PM trợ lý hoàn phí |

**Đề xuất: Go có điều kiện** cho pilot noi_dia + hang_nang, chia theo nhân viên 20 + 20. Con số bất lợi đã tính: xem lại 100% làm chi phí lên 0,98–1,03× (gần như không tiết kiệm), và power chỉ 0,64 ở mức 5 điểm.

- Có khoá chống trùng và đối soát sổ cái mỗi giờ (ca lỗi 7, 20), ngưỡng 0 ca hoàn trùng khi chạy thử nội bộ. Phụ trách: Kỹ sư trưởng agent · Kiểm tra: 2026-12-04.
- Ký chấp nhận mức chênh 6 điểm và rủi ro power 0,64 nếu tác động thật chỉ 5 điểm. Phụ trách: Giám đốc vận hành LogiX-VN · Kiểm tra: 2026-12-04.
- Bật đủ 10 event có trace_id; thay phút simulated bằng phút đo thật từ `staff_review_decision`, `staff_rework_completed` sau tuần 1 và tính lại mục 1–3. Phụ trách: PM trợ lý hoàn phí · Kiểm tra: 2026-12-14.
- Có kế hoạch giảm xem lại theo bậc; nếu cuối bước 0,25 vẫn xem lại > 50% hoặc mỗi lần xem lại > 5,1 phút thì không mở bước 0,50. Phụ trách: Trưởng nhóm CSKH · Kiểm tra: 2026-12-21.
