"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
# TODO CP1: viết ba hàm dưới đây cho tới khi kiem_tra_dap_an_biet_truoc() in ĐẠT.
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    # Lần chạy thứ i xảy ra khi i-1 lần trước đều sai: P = (1-p)^(i-1).
    # Cộng i = 1..k (cấp số nhân) → (1 - (1-p)^k) / p. Khi k → ∞ còn 1/p.
    if k is None:
        return 1 / p
    return (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    # Chỉ thất bại khi cả k lần đều sai: (1-p)^k.
    if k is None:
        return 1.0
    return 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    # Tử số: trả tiền cho MỌI lần chạy (kể cả lần sai). Mẫu số: chỉ việc thành công.
    # Hai vế cùng có (1 - (1-p)^k) nên triệt tiêu → luôn bằng 1/p, không phụ thuộc k.
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# TODO CP1: viết mo_hinh; CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    reqs = reqs.copy()
    # Chỉ giữ lần chạy của các yêu cầu đang xét (để A3 lọc theo loai là đủ).
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        # Giới hạn số lần chạy: bỏ lần chạy vượt giới hạn; yêu cầu cần nhiều lần hơn
        # coi như chuyển nhân viên (không còn phút xem lại / làm lại của trợ lý).
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0

    # Tử số: MỌI lần chạy, kể cả lần lỗi. Giá token tính trên 1.000 token.
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    # Giờ nhân viên (simulated).
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    # Mẫu số: chỉ đếm yêu cầu thành công.
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())
    return dict(
        token=tien_token.sum(),
        tool=tien_tool.sum(),
        chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
        xem_lai=xem_lai,
        lam_lai=lam_lai,
        tong=tong,
        thanh_cong=thanh_cong,
        cps=tong / thanh_cong,
        hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs),
    )


def chi_phi_co_dinh(cps_pham_vi, ti_le_tc, khoi_luong_thang=45000, co_dinh=40_000_000):
    """A4: cộng chi phí cố định/tháng vào chi phí mỗi việc thành công."""
    viec_tc_thang = khoi_luong_thang * ti_le_tc
    cd_moi_viec = co_dinh / viec_tc_thang
    return viec_tc_thang, cd_moi_viec, cps_pham_vi + cd_moi_viec


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    print(f'  A1: {so_lan_chay_ky_vong(0.8, 2):.2f} · {so_lan_chay_ky_vong(0.8):.2f} · '
          f'{he_so_chi_phi_moi_viec_thanh_cong(0.8, 3):.2f}')

    print('\n== A2 · Mô hình chi phí từ trace (xem_lai, lam_lai, tong, cps: simulated) ==')
    ket_qua = mo_hinh(runs, reqs)
    for ten, gia_tri in ket_qua.items():
        print(f'{ten:15s} {gia_tri:>14,.1f}')
    print(f"Phút xem lại: {reqs['phut_xem_lai_simulated'].sum()} · phút làm lại: "
          f"{reqs['phut_lam_lai_simulated'].sum()} · lần gọi tool: {runs['tool_calls'].sum()}")
    print(f"cps / hoá đơn mỗi yêu cầu = {ket_qua['cps'] / ket_qua['hoa_don_moi_yc']:.1f} lần")
    for khoan in ['token', 'tool', 'xem_lai', 'lam_lai']:
        print(f"  tỉ trọng {khoan:8s} {ket_qua[khoan] / ket_qua['tong']:6.1%}")
    khong_tc = len(reqs) - ket_qua['thanh_cong']
    he_thong = (ket_qua['tong'] + khong_tc * BASELINE) / len(reqs)
    print(f'Chi phí cả hệ thống mỗi yêu cầu (cộng {khong_tc} ca không thành công × 12.000 đ): '
          f'{he_thong:,.0f} đ = {he_thong / BASELINE:.2f}× [simulated]')

    # CP1 · Nhiệm vụ A3: tính lại theo từng giá trị của cột loai.
    print('\n== A3 · Theo loại yêu cầu (cps: simulated) ==')
    print(f"{'loai':10s} {'so_yc':>6s} {'ti_le_tc':>9s} {'lan/yc':>7s} {'cps':>9s} {'so_12k':>7s}")
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        r = reqs[reqs['loai'] == loai]
        kq = mo_hinh(runs, r)
        so_lan = runs['request_id'].isin(r['request_id']).sum() / len(r)
        print(f"{loai:10s} {len(r):6d} {kq['thanh_cong'] / len(r):9.1%} {so_lan:7.2f} "
              f"{kq['cps']:9,.0f} {kq['cps'] / BASELINE:6.2f}×")
    # Chạy lại có giúp không: tỉ lệ ok theo từng lần thử.
    ok_theo_lan = (runs.merge(reqs[['request_id', 'loai']], on='request_id')
                   .assign(ok=lambda d: (d['status'] == 'ok').astype(float))
                   .pivot_table(index='loai', columns='attempt', values='ok', aggfunc='mean'))
    print('\nTỉ lệ ok theo lần thử:')
    print(ok_theo_lan.map(lambda x: f'{x:.1%}').to_string())

    # CP1 · Nhiệm vụ A4: chi phí cố định 40 triệu đ/tháng, phạm vi noi_dia + hang_nang.
    print('\n== A4 · Chi phí cố định, phạm vi noi_dia + hang_nang (simulated) ==')
    pham_vi = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    kq_pv = mo_hinh(runs, pham_vi)
    ti_le_tc_mau = kq_pv['thanh_cong'] / len(reqs)   # theo đề: 900 / 1.200 của mẫu
    print(f"Phạm vi: {len(pham_vi)} yêu cầu, {kq_pv['thanh_cong']} thành công, "
          f"cps = {kq_pv['tong']:,.0f} / {kq_pv['thanh_cong']} = {kq_pv['cps']:,.0f} đ")
    for nhan, kl in [('45.000 yêu cầu/tháng', 45000), ('Một nửa khối lượng', 22500)]:
        viec, cd, tong_cd = chi_phi_co_dinh(kq_pv['cps'], ti_le_tc_mau, kl)
        print(f'{nhan:22s} việc TC/tháng {viec:>9,.0f} · cố định/việc {cd:>7,.0f} đ · '
              f'cps + cố định {tong_cd:>7,.0f} đ = {tong_cd / BASELINE:.2f}×')
    # CP2 · Nhiệm vụ B1: đổi từng yếu tố, mỗi kịch bản là một lần gọi mo_hinh.
    print('\n== B1 · Đổi từng yếu tố (cps: simulated) ==')
    goc = ket_qua['cps']
    kich_ban = {
        'Giá token gấp đôi':      dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa': dict(gia_vao=13, gia_ra=65),
        'Xem lại gấp đôi':        dict(he_so_xem_lai=2),
        'Xem lại giảm một nửa':   dict(he_so_xem_lai=0.5),
        'Làm lại gấp đôi':        dict(he_so_lam_lai=2),
        'Làm lại giảm một nửa':   dict(he_so_lam_lai=0.5),
        'Lương tăng 25%':         dict(luong_phut=2500),
        'Tối đa 2 lần chạy':      dict(max_lan_chay=2),
        'Chỉ 1 lần chạy':         dict(max_lan_chay=1),
    }
    print(f"{'Gốc (A2)':25s} {goc:8,.0f}")
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        print(f'{ten:25s} {cps:8,.0f} {(cps / goc - 1) * 100:+6.1f}%')

    # B2: đổi một cặp. Mô hình cộng tuyến tính → tác động bằng tổng hai tác động riêng.
    cps_cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)['cps']
    print(f"\n== B2 · Token ×2 và xem lại ×2: {cps_cap:,.0f} đ ({(cps_cap / goc - 1) * 100:+.1f}%) ==")

    # B3: chi phí cả hệ thống = chi phí trợ lý + 12.000 đ × số yêu cầu nhân viên phải làm thay.
    print('\n== B3 · Giới hạn số lần chạy (simulated) ==')
    print(f"{'gioi_han':>8s} {'tong_tro_ly':>12s} {'khong_tc':>9s} {'ca_he_thong':>12s} {'cps':>7s}")
    for k in [1, 2, 3]:
        kq = mo_hinh(runs, reqs, max_lan_chay=k)
        khong_tc = len(reqs) - kq['thanh_cong']
        print(f"{k:8d} {kq['tong']:12,.0f} {khong_tc:9d} "
              f"{kq['tong'] + khong_tc * BASELINE:12,.0f} {kq['cps']:7,.0f}")

    # B4: xem lại 100% trong phạm vi noi_dia + hang_nang (đề cho 5 phút/lần xem lại, 9 phút/ca làm lại).
    print('\n== B4 · Xem lại 100%, phạm vi noi_dia + hang_nang (simulated) ==')
    runs_pv = runs[runs['request_id'].isin(pham_vi['request_id'])]
    so_xem = runs_pv.loc[runs_pv['status'] == 'ok', 'request_id'].nunique()
    so_lam_lai = int((pham_vi['ket_qua'] == 'lam_lai').sum())
    tok_tool = kq_pv['token'] + kq_pv['tool']
    tc_pv = kq_pv['thanh_cong']
    phut_lam_lai_tb = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated']
    print(f'Yêu cầu có lần chạy ok: {so_xem} · ca lam_lai: {so_lam_lai} · token+tool: {tok_tool:,.0f} đ')
    print(f'Phút làm lại thật trên ca lam_lai: TB {phut_lam_lai_tb.mean():.1f}, '
          f'trung vị {phut_lam_lai_tb.median():.1f}')
    for phut_lam in [9, round(phut_lam_lai_tb.mean(), 1)]:
        tien_xem = so_xem * 5 * LUONG_PHUT
        tien_lam = so_lam_lai * phut_lam * LUONG_PHUT
        tong_b4 = tok_tool + tien_xem + tien_lam
        # Hoà vốn: số phút xem lại tối đa để cps = 12.000 đ.
        hoa_von = (BASELINE * tc_pv - tok_tool - tien_lam) / (so_xem * LUONG_PHUT)
        print(f'làm lại {phut_lam:4} phút/ca: tổng {tong_b4:,.0f} đ → cps {tong_b4 / tc_pv:,.0f} đ '
              f'= {tong_b4 / tc_pv / BASELINE:.2f}× · hoà vốn khi xem lại ≤ {hoa_von:.1f} phút')
    # CP4 · Nhiệm vụ D1: cỡ mẫu (baseline 0,70; +5 điểm; alpha 0,05; power 0,8; ICC 0,02).
    from statistics import NormalDist
    from statsmodels.stats.proportion import proportion_effectsize
    from statsmodels.stats.power import NormalIndPower

    def co_mau(p1, p2, alpha=0.05, power=0.8):
        """Cỡ mẫu mỗi nhóm khi so hai tỉ lệ (công thức trong docs/du_lieu_va_cong_thuc.md)."""
        za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
        pb = (p1 + p2) / 2
        return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                          + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)

    def he_so_thiet_ke(m, icc=0.02):
        return 1 + (m - 1) * icc

    ICC = 0.02
    print('\n== D1 · Cỡ mẫu ==')
    n5 = co_mau(0.70, 0.75)
    n_sm = NormalIndPower().solve_power(proportion_effectsize(0.75, 0.70), alpha=0.05, power=0.8)
    print(f'a) Theo yêu cầu: {n5} mỗi nhóm (statsmodels, arcsin: {math.ceil(n_sm)})')
    de75 = he_so_thiet_ke(75, ICC)
    nb = math.ceil(n5 * de75)
    nv = math.ceil(nb / 75)
    print(f'b) Theo nhân viên m=75: DE = {de75:.2f}, n = {nb} mỗi nhóm → {nv} người/nhóm, '
          f'tổng {2 * nv} {">" if 2 * nv > 40 else "≤"} 40 nhân viên')
    print(f'c) 20 nhân viên/nhóm: hiệu dụng tối đa < c/ICC = {20 / ICC:,.0f} '
          f'({"đạt" if 20 / ICC >= n5 else "không đạt"} {n5})')
    print(f'd) 6 depot/nhóm: hiệu dụng tối đa < {6 / ICC:,.0f}')
    n6 = co_mau(0.70, 0.76)
    m_min = math.ceil(n6 * (1 - ICC) / (20 - n6 * ICC))   # giải 20m / (1 + (m-1)ICC) ≥ n6
    print(f'e) Mức chênh 6 điểm: {n6} mỗi nhóm; 20 người/nhóm cần m ≥ {m_min} yêu cầu/người '
          f'(DE {he_so_thiet_ke(m_min, ICC):.2f}, hiệu dụng {20 * m_min / he_so_thiet_ke(m_min, ICC):,.0f})')
    # Con số bất lợi: thiết kế cho 6 điểm mà tác động thật chỉ 5 điểm thì power còn bao nhiêu?
    pw = NormalIndPower().power(proportion_effectsize(0.75, 0.70), nobs1=n6, alpha=0.05)
    print(f'   Power nếu tác động thật chỉ +5 điểm với {n6}/nhóm: {pw:.2f}')

    # Tỉ lệ hiện tại của các chỉ số an toàn / sử dụng, trước khi đặt luật dừng.
    print('\n== Tỉ lệ hiện tại trong đợt chạy thử (đặt ngưỡng luật dừng) ==')
    print(f"mo_lai_trong_7_ngay: toàn mẫu {reqs['mo_lai_trong_7_ngay'].mean():.2%} "
          f"({reqs['mo_lai_trong_7_ngay'].sum()}/{len(reqs)}), phạm vi noi_dia+hang_nang "
          f"{pham_vi['mo_lai_trong_7_ngay'].mean():.2%}")
    print(f"Chỉ số chính (đóng 24h, không mở lại 7 ngày) trong phạm vi: "
          f"{((pham_vi['dong_trong_24h'] == 1) & (pham_vi['mo_lai_trong_7_ngay'] == 0)).mean():.2%}")
    xem = pham_vi[pham_vi['duoc_xem_lai'] == 1]
    print(f"Được xem lại trong phạm vi: {len(xem)}/{len(pham_vi)} = {len(xem) / len(pham_vi):.1%}; "
          f"quyết định bỏ: {(xem['quyet_dinh_xem_lai'] == 'bo').mean():.1%}, "
          f"sửa: {(xem['quyet_dinh_xem_lai'] == 'sua').mean():.1%}")
