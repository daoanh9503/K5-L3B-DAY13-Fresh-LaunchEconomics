# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: Fresh (làm một mình)
- Lớp: L3B
- Thành viên: xem `TEAM.md` (Đào Thị Ngọc Ánh, 2A202603790)

## 2. Mục tiêu và cách tiếp cận

Dựng hồ sơ launch v0 cho trợ lý hoàn phí LogiX-VN để Gate 2a quyết định có chạy pilot hay không. Cách làm: tính mọi con số bằng `src/lab13.py` trên hai file CSV giả lập, đối chiếu với số tự kiểm tra trong hướng dẫn, rồi ghép A–D thành một trang hồ sơ. Mọi số từ cột `_simulated` ghi nhãn simulated.

## 3. Giải pháp

- **A · Chi phí mỗi việc thành công** ([bang_chi_phi.md](bang_chi_phi.md)): tử số cộng token, tool của mọi lần chạy (kể cả lỗi) và giờ nhân viên; mẫu số chỉ đếm `ket_qua == 'thanh_cong'`. Tách theo `loai` và cộng chi phí cố định 40 triệu đ/tháng.
- **B · Độ nhạy** ([bang_chi_phi.md](bang_chi_phi.md)): gọi lại `mo_hinh` cho 9 kịch bản, một cặp, giới hạn 1/2/3 lần chạy, và xem lại 100%.
- **C · Bảng lỗi** ([bang_loi.md](bang_loi.md)): gắn nhãn 20 ca theo năm loại Google PAIR, theo nguyên nhân gốc; bảng khắc phục 5 ca với ngưỡng đo được và vai trò phụ trách.
- **D · Pilot** ([pilot_plan.yaml](pilot_plan.yaml)): tính cỡ mẫu ba cách chia trước khi chọn; chọn chia theo nhân viên 20 + 20, chấp nhận mde 6 điểm.
- **E · Chỉ số và hồ sơ** ([chi_so.md](chi_so.md), [ho_so_launch_v0.md](ho_so_launch_v0.md)): ba chỉ số tính thử, 10 event có trace_id, 3 dòng rủi ro kinh tế, hồ sơ bảy mục.

## 4. Kết quả

- Chi phí mỗi việc thành công 4.472 đ [simulated], gấp 16,3 lần hoá đơn token + tool chia số yêu cầu; giờ nhân viên chiếm 92,5%.
- Yếu tố nhạy nhất: số ca làm lại (±51,8%), tỉ lệ xem lại (±40,7%), lương (+23,1%) [simulated]; giá token chỉ ±5,6%.
- Phạm vi noi_dia + hang_nang: 4.599 đ = 0,38× của 12.000 đ đã cộng cố định [simulated]; quoc_te 1,88× nên loại. Xem lại 100% thì 0,98–1,03× [simulated].
- Pilot: chia theo nhân viên 20 + 20, mde 6 điểm (859 hiệu dụng mỗi nhóm, ≥ 299 yêu cầu/người); power 0,64 nếu tác động thật là 5 điểm.
- Chỉ số trong đợt chạy thử: chính 82,83%, bỏ qua gợi ý 27,12%, mở lại 7 ngày 4,25%.
- **Đề xuất: Go có điều kiện** cho pilot noi_dia + hang_nang, bốn điều kiện có người phụ trách và ngày kiểm tra.
- Kết quả duyệt chéo từ hội đồng: chưa có (xem mục 5).

## 5. Khó khăn và cách xử lý

- **Làm một mình thay vì nhóm 4 người.** Một người đảm nhận cả bốn vai. Hai phần cần người khác chưa làm được đúng yêu cầu: bộ nhãn thứ 2 ở nhiệm vụ C (đồng thuận chưa tính được, chỉ có một bộ nhãn) và duyệt chéo Gate 2a (`phieu_cham.md` để trống, chưa có nhóm để chấm). Đã ghi rõ trong `bang_loi.md` và đang hỏi coach cách xử lý; không tự tạo bộ nhãn hay phiếu chấm thay.
- **Cài môi trường bị lỗi.** Lần `pip install` đầu bị ngắt giữa chừng, để lại file hỏng ("source code string cannot contain null bytes"); xoá `.venv` và cài lại thì chạy được.
- **Tiếng Việt trên Windows.** `python lab13.py` lỗi `UnicodeEncodeError` khi in ra cửa sổ lệnh cp1252; thêm `sys.stdout.reconfigure(encoding='utf-8')`. Lệnh kiểm tra `yaml.safe_load(open(...))` trong checklist cũng lỗi bảng mã trên Windows (cả file mẫu gốc); chạy với `PYTHONUTF8=1` thì đọc được.
- **Push lỗi chứng chỉ SSL** ("unable to get local issuer certificate"); push bằng `git -c http.sslBackend=schannel push`, vẫn giữ kiểm tra SSL.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md`.

## 7. Hạn chế và hướng cải thiện

- Chi phí dựa trên phút xem lại và làm lại giả lập; pilot phải thay bằng phút đo thật sau tuần 1 rồi tính lại.
- Đợt chạy thử không có đối chứng, nên chỉ số 82,83% chỉ mô tả, không chứng minh tác động.
- Với 40 nhân viên không đủ mẫu cho +5 điểm; chấp nhận mde 6 điểm và power 0,64 ở mức 5 điểm.
- Thiếu bộ nhãn độc lập thứ 2 và phần chấm chéo; cần bổ sung nếu coach cho ghép với nhóm khác.

## 8. Tài liệu tham khảo

- Đề bài và hướng dẫn Lab 13 trong `docs/`.
- Erol và cộng sự, *Cost-of-Pass: An Economic Framework for Evaluating Language Models*, arxiv.org/abs/2504.13359.
- Google PAIR, *People + AI Guidebook*, chương "Errors + Graceful Failure".
- statsmodels, `NormalIndPower` và `proportion_effectsize`.
