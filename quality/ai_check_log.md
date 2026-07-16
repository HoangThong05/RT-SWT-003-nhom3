# AI Writing Check Log

**Paper:** Evaluating Qwen2.5-7B Few-shot Prompting Against GPT-4o Threshold for Bug Report Quality Assessment
**Nhóm:** RT-SWT-003-nhom3 (SWT302 — Research-Based Learning in Software Testing)
**Ngày check cuối:** 2026-07-16
**Công cụ sử dụng:** ZeroGPT (zerogpt.com), SciSpace AI Detector (scispace.com/ai-detector)

## Quy trình kiểm tra

Mỗi section được copy riêng lẻ từ bản PDF đã compile (không copy trực tiếp mã LaTeX), loại bỏ các phần không thuộc phạm vi đánh giá văn phong: bảng số liệu (Table), hình ảnh minh họa (Figure), code listing (prompt template), và câu "roadmap" liệt kê cấu trúc bài viết (`The remainder of this paper is structured as follows...`) — vì các phần này tuân theo định dạng bắt buộc của thể loại paper khoa học, không phản ánh văn phong thật của người viết.

Mỗi section được chạy qua tối thiểu 2 công cụ độc lập, theo đúng phân công RBL-5b.

## Kết quả chi tiết

| Section | ZeroGPT % | SciSpace % | Trung bình | Đoạn cần viết lại | Đã sửa |
|---------|-----------|------------|------------|--------------------|--------|
| §1 Introduction | 14.7% | 17% | 15.85% | Không có đoạn vượt ngưỡng cảnh báo. | ✅ |
| §2 Related Work | 3.6% | 1% | 2.3% | Không phát hiện nguy cơ AI đáng kể. | ✅ |
| §3 Methodology | 9.7% | 9% | 9.35% | Không phát hiện nguy cơ AI đáng kể. | ✅ |
| §4 Results | 11.9% | 5% | 8.45% | Không phát hiện nguy cơ AI đáng kể. | ✅ |
| §5 Discussion | 0.6% | 1% | 0.8% | Không phát hiện nguy cơ AI đáng kể. | ✅ |
| §6 Threats to Validity | 2.8% | 0% | 1.4% | Không phát hiện nguy cơ AI đáng kể. | ✅ |
| §7 Conclusion | 3.6% | 0% | 1.8% | Không phát hiện nguy cơ AI đáng kể. | ✅ |

## Diễn giải theo thang đánh giá RBL-5b

| % AI (trung bình 2 công cụ) | Đánh giá |
|---|---|
| < 20% | Tốt |
| 20–50% | Cần xem lại |
| 50–80% | Không chấp nhận |
| > 80% | Không chấp nhận |

Toàn bộ 7/7 section đạt mức **< 20% — Tốt**.

## Kiểm tra bổ sung (Bước 2–4 theo RBL-5b)

- [x] **Đọc kiểu "tester"**: từng thành viên đọc to phần mình phụ trách, xác nhận không có câu "nghe hay nhưng không nói gì cụ thể".
- [x] **Citation density**: §1, §2, §3, §5 — mọi claim về prior work đều có `\cite{}`; §4 và §7 không cite (đúng quy ước, vì là số liệu/kết luận của nhóm).
- [x] **Kiểm tra số liệu**: mọi số trong §4 Results trace được về `full_metrics_output_FINAL.csv` và `RQ1_results_FINAL.md`; số liệu Abstract, §4, §5 khớp nhau tuyệt đối (không thay đổi khi diễn giải).

## Kết luận

Tất cả 7 section của paper đã được kiểm tra bằng ZeroGPT và SciSpace AI Detector. Toàn bộ đều đạt mức **Human / Essentially Human**, không có section nào vượt ngưỡng cảnh báo theo hướng dẫn RBL-5b. Nội dung, số liệu thực nghiệm, và trích dẫn học thuật được giữ nguyên trong suốt quá trình hiệu chỉnh văn phong — chỉ điều chỉnh cách diễn đạt câu, không thay đổi số liệu hay ý nghĩa khoa học.

**Kết luận cuối cùng:** Đạt yêu cầu, không cần chỉnh sửa thêm.
