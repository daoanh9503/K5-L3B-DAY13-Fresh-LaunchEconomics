# Báo cáo cá nhân — DaoThiNgocAnh-2A202603790

## 1. Thông tin thành viên

- Họ tên: Đào Thị Ngọc Ánh
- MSSV: 2A202603790
- Email:
- Vai trong nhóm: làm một mình, đảm nhận cả bốn vai (người viết code, người kiểm số, người gắn nhãn 1, người giữ hồ sơ)

## 2. Phần việc phụ trách

Toàn bộ nhiệm vụ A–E: `src/lab13.py`, `bang_chi_phi.md`, `bang_loi.md`, `pilot_plan.yaml`, `chi_so.md`, `ho_so_launch_v0.md`, `group_report.md`, `TEAM.md`. Chưa làm được: bộ nhãn thứ 2 (nhiệm vụ C) và `phieu_cham.md` (duyệt chéo), vì cần người hoặc nhóm khác.

## 3. Đóng góp cụ thể

- A: ba hàm A1 (1,20 · 1,25 · 1,25 ĐẠT), `mo_hinh`, chi phí mỗi việc thành công 4.472 đ [simulated], tách theo loại, cộng chi phí cố định.
- B: 9 kịch bản độ nhạy, xếp hạng ba yếu tố, so giới hạn 1/2/3 lần chạy, kịch bản xem lại 100%.
- C: tự chọn nhãn cho 20 ca lỗi; khớp nhãn tham khảo 19/20 (ca 20 chọn Ngầm, nhãn tham khảo là Hệ thống).
- D: cỡ mẫu a–e, chọn chia theo nhân viên 20 + 20 với mde 6 điểm, ba luật dừng.
- E: ba chỉ số tính thử, danh sách event, rủi ro kinh tế, hồ sơ launch v0 với đề xuất Go có điều kiện.

## 4. Bằng chứng

- Commit `a799238` (CP1, CP2), `daf4556` (CP3), `27cd58b` (CP4), `b8bf3d6` (CP5) trên nhánh `main`.
- `cd src && python lab13.py` in "Ba phép thử đáp án biết trước: ĐẠT" và các bảng A2, A3, A4, B1–B4, D1, E1.
- `pilot_plan.yaml` đọc được bằng `yaml.safe_load`, không còn dấu `?` ngoài chú thích.

## 5. Công cụ AI đã dùng

Claude (Claude Code, chạy trên máy cá nhân), dùng vào:

- **Code:** viết các hàm A1, `mo_hinh`, phần in bảng A3, A4, B, D1, E1 trong `src/lab13.py`, theo công thức trong `docs/du_lieu_va_cong_thuc.md`.
- **Nhiệm vụ C:** Claude đặt câu hỏi gợi ý theo định nghĩa năm loại lỗi (không đưa đáp án); tôi tự chọn nhãn từng ca. Ca 1, 5, 8 tôi đổi nhãn sau câu hỏi gợi ý. Claude soạn nháp bảng khắc phục 5 ca.
- **Soạn nháp hồ sơ:** `pilot_plan.yaml`, `chi_so.md`, `ho_so_launch_v0.md`, báo cáo nhóm, từ số do `lab13.py` tính ra.
- **Xử lý lỗi môi trường:** cài lại `.venv`, lỗi bảng mã tiếng Việt trên Windows, lỗi SSL khi push.

Cách tự kiểm tra:

- Chạy `lab13.py`: ba phép thử A1 in ĐẠT; mọi số A2, A3, A4, B1–B4, D1, E1 khớp số tự đối chiếu trong `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md` (lệch ≤ 2%).
- Kiểm tra `pilot_plan.yaml` bằng `yaml.safe_load` và tìm dấu `?`; tìm từ bị cấm theo quy tắc 5 trong `README.md` ở `report/team/`.
- Nhãn lỗi chỉ đối chiếu với nhãn tham khảo sau khi đã gắn xong cả 20 ca.
- (Bổ sung: những phần tôi tự đọc lại và sửa.)

## 6. Tự đánh giá

- Làm đủ A, B, D, E với số khớp đáp án; hiểu vì sao tử số tính mọi lần chạy còn mẫu số chỉ đếm việc thành công, và vì sao chia theo cụm làm cỡ mẫu hiệu dụng bị chặn bởi c ÷ ICC.
- Nhiệm vụ C thiếu bộ nhãn độc lập thứ 2; phần duyệt chéo chưa làm. Cả hai đang chờ coach hướng dẫn.
- Dựa nhiều vào AI để viết code và soạn nháp; cần tự giải thích lại được các con số khi hội đồng hỏi.
