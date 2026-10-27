"""EDL v3: every segment sits inside ONE stable shot (shots.json, OCR-clean), >= 3 s, 0.25 s margins."""
import json
CLEAN = {i: (r[0], r[2], r[3]) for i, r in enumerate(json.load(open('clean.json')))}
CLEAN['TEAM'] = (1, 405.9, 411.3)      # doctors around table (checked by eye, no text)
CLEAN['XRAY'] = (3, 107.0, 113.4)      # specialists reading X-rays
PLAN = [  # (t0, shot, note)
 (0.0, 177, 'phòng họp, ghế dưới đèn'), (6.2, 213, 'bác sĩ cúi nhìn trái tim'), (9.6, 188, 'nhóm bác sĩ quanh bàn'),
 (13.8, 12, 'hồ sơ ca A/B/C, ống nghiệm'), (17.0, 203, 'bác sĩ khoanh tay phản bác'), (20.0, 182, 'kính lúp đỏ soi hồ sơ'),
 (25.3, 18, 'bảng giá thiết bị'), (30.6, 11, 'bác sĩ lặng lẽ đọc hồ sơ'), (35.4, 165, 'kiểm tra hồ sơ'),
 (40.2, 22, 'dấu tích xác nhận'), (44.9, 227, 'đóng dấu chẩn đoán'), (47.9, 'TEAM', 'đội hội chẩn'),
 (51.1, 177, 'ghế trống dưới đèn'), (54.5, 142, 'những hình nhân'), (57.5, 184, 'những chiếc mũ'),
 (62.9, 1, 'toà nhà Microsoft'), (66.5, 41, 'Science'), (71.3, 43, 'bài thi A+'), (75.3, 42, 'bác sĩ với tablet'),
 (78.7, 207, 'hình người phát sáng (Tập 34)'), (82.1, 208, 'tay robot đưa thuốc (Tập 33)'), (86.3, 3, 'bài thi A+'),
 (89.7, 209, 'phòng khám trống'), (92.7, 169, 'kính lúp'), (96.8, 16, 'tay vẽ mạng lưới'),
 (100.4, 230, 'nhà trên núi'), (103.7, 79, 'bác sĩ đeo tai nghe hội chẩn từ xa'),
 (108.7, 92, 'não AI bị gạch'), (112.9, 98, 'khối điều phối'), (116.6, 100, 'khối và vệ tinh'), (119.9, 184, 'những chiếc mũ'),
 (134.2, 145, 'bo mạch'), (138.0, 97, 'não trên chồng sách'), (143.0, 212, 'radar dò lỗi'),
 (146.3, 226, 'các bác sĩ bên màn hình'), (151.3, 140, 'hai bác sĩ xem X-quang'),
 (157.1, 1, 'Microsoft'), (165.5, 228, 'bác sĩ khám bệnh nhân'), (168.8, 'TEAM', 'hội đồng chuyên khoa'), (171.8, 194, 'hai bác sĩ chuyên khoa'),
 (174.9, 1, 'nền mờ biểu đồ'),
 (203.1, 9, 'sách và giấy'), (207.0, 96, 'hồ sơ và đơn thuốc'), (211.6, 221, 'laptop và bệnh án'), (214.6, 215, 'giường bệnh trống'),
 (217.7, 106, 'bệnh viện, xe cấp cứu'), (222.0, 72, 'khu bệnh viện'), (227.4, 108, 'giường bệnh và máy chủ'), (230.5, 111, 'cửa cấm AI'),
 (233.8, 1, 'Microsoft'), (243.1, 154, 'người và chữ 4X'),
 (254.2, 79, 'nền mờ bản đồ'), (262.4, 115, 'nền mờ bản đồ'), (268.4, 129, 'bác sĩ bên máy tính'),
 (271.4, 13, 'đồng hồ, cà phê'), (274.8, 117, 'robot và bác sĩ'), (279.0, 20, 'điều dưỡng bên máy tính'),
 (282.2, 220, 'bác sĩ trẻ tuyến dưới với tablet'), (288.0, 77, 'tablet hồ sơ'), (291.8, 13, 'đồng hồ 15 phút'),
 (295.2, 76, 'chuyên gia chỉ tay'), (298.2, 163, 'bác sĩ và AI'), (304.2, 118, 'AI và hội đồng'), (308.1, 134, 'luồng phân loại'),
 (314.1, 197, 'cây cầu nối hai tuyến'), (322.5, 172, 'cây cầu'), (328.2, 227, 'đóng dấu'), (332.8, 80, 'ký thẩm định'),
 (339.5, 122, 'đường núi về bệnh viện'), (345.1, 230, 'nhà trên núi'), (348.4, 243, 'bác sĩ vùng cao'), (352.3, 128, 'mũ tốt nghiệp'),
 (355.9, 179, 'giảng trên bảng não'), (359.6, 127, 'thầy trò cùng sách'), (363.2, 241, 'bác sĩ tự tin'),
 (367.1, 81, 'lớp học'), (373.0, 168, 'ôm đầu trước màn hình'), (376.9, 193, 'lịch 2036'), (384.0, 52, 'đồ thị đi xuống'),
 (387.5, 180, 'robot gia sư'), (393.8, 23, 'số 4 và kính lúp'), (397.0, 192, 'nền mờ bốn câu hỏi'),
 (410.5, 184, 'những chiếc mũ'), (417.0, 237, 'robot và bộ não'), (420.3, 239, 'cáp quang tới bản làng'),
 (423.6, 194, 'hai bác sĩ'), (428.3, 245, 'bàn tròn'), (434.6, 191, 'đồng hồ 02:00 AM'),
 (441.5, 60, 'hai người cầm bệnh án'), (445.0, 11, 'bác sĩ và AI'), (448.4, 27, 'bác sĩ trên cầu'), (454.0, 28, 'cây cầu, ánh sáng'),
]
DUR = 464.0
EDL, err = [], []
for k, (t0, sid, note) in enumerate(PLAN):
    t1 = PLAN[k + 1][0] if k + 1 < len(PLAN) else DUR
    c, a, b = CLEAN[sid]; d = t1 - t0
    if d < 3.0 - 1e-6 and t1 < DUR: err.append(f'{t0}: {d:.1f}s < 3s')
    if d > (b - a) - 0.3 + 1e-6: err.append(f'{t0}: {d:.1f}s > shot {sid} ({b-a:.1f}s)')
    s = a + 0.15 + max(0, ((b - a) - 0.3 - d) / 2) * 0.5   # sit inside the shot, slightly centred
    EDL.append((t0, c, round(s, 2), note))
if __name__ == '__main__':
    print('\n'.join(err) or 'EDL OK', len(EDL), 'segments')
