# notes.md — Experiment Technical Decisions & Error Log
# Nhóm 3 — SWT302 — Bug Report Quality Assessment with LLM

---

## 1. Thông tin chung

| Thông số | Giá trị |
|----------|---------|
| Model | `unsloth/Qwen2.5-7B-Instruct` |
| Prompt strategy | 3-shot, Alpaca-LoRA template (E02 Listing 2) |
| Temperature | 0.01 (thấp nhất cho phép — model yêu cầu >0) |
| Sampling | `do_sample=False` (greedy decoding) |
| Max new tokens | 512 |
| Nền tảng | Kaggle Notebook |
| GPU | Tesla T4 (đổi từ P100 — xem mục 3.1) |
| Random seed dataset split | 42 |
| N pilot | 80 |
| N full run | 262 |

---

## 2. Quyết định kỹ thuật về Dataset

### 2.1 Nguồn dữ liệu
- Dataset gốc: `GindeLab/Ease_2025_AI_model` (Bugzilla/Mozilla) — N=3,966 sau khi lọc
- File cục bộ: `Plus14_filtered_bug_report_scores_Summary.xlsx`
- Chiến lược split: 80/10/10 với `random_state=42`
- Test set dùng cho RQ1: 10% → N≈397 (thực tế sau drop incomplete: **N=262**)

### 2.2 Lý do N=262 thay vì N≈397
- Sau bước filter các sample có `qwen_output` rỗng hoặc không đúng format 4 section (S2R/ER/AR/Additional Information), còn lại 262 samples hợp lệ.
- Tỷ lệ valid: 262/397 = **66.0%** — ghi nhận là deviation so với proposal (§5 dự kiến ≈397).
- Không tự điền hay bỏ qua sample invalid — đánh dấu và loại trước khi tính metric, đúng theo RBL-4 §8.2.

---

## 3. Vấn đề kỹ thuật gặp phải & cách xử lý

### 3.1 GPU không tương thích (LR — Tuần 7)
**Vấn đề:** Lần chạy đầu trên GPU P100 báo lỗi:
```
Tesla P100-PCIE-16GB with CUDA capability sm_60 is not compatible
with the current PyTorch installation.
Some parameters are on the meta device.
```
**Xử lý:** Đổi Kaggle Accelerator từ P100 sang **T4** (Settings → Accelerator). Model load đầy đủ lên GPU, chạy ổn định cho toàn bộ pilot và full run.
**Ghi chú:** Đây là lý do slide DG đề cập "Kaggle GPU T4" thay vì P100 như trong proposal §8.1 ban đầu. Không cần amendment vì là thay đổi hardware tương đương, không ảnh hưởng đến RQ/metric/threshold.

### 3.2 Warning `do_sample=False` (LR — Tuần 7)
**Cảnh báo:**
```
The following generation flags are not valid and may be ignored: ['temperature', 'top_p', 'top_k']
```
**Nguyên nhân:** `do_sample=False` kích hoạt greedy decoding — các flag sampling bị ignore.
**Xử lý:** Bỏ qua — không ảnh hưởng output (đã verify 100% samples có đủ 4 section).

### 3.3 CTQRS scorer — Word-list nhiễu (MS — Tuần 8)
**Vấn đề:** CTQRS ban đầu cho kết quả ~93.75% — cao bất thường.
**Nguyên nhân (Debug 1-3):**
- `INTERFACE_ELEMENT_WORDS` và `USER_DIRECT_VERBS` chứa từ ngắn <3 ký tự (vd: "a", "in", "on") và câu dài bị lẫn vào — gây match giả tràn lan ở RA1/RA2/RA3.
**Fix:** Lọc word-list: chỉ giữ token 3–29 ký tự, không chứa khoảng trắng.
**File fix:** `ctqrs_scorer_v2_fixed.py`

### 3.4 CTQRS scorer — RM3 punctuation luôn fail (MS — Tuần 8)
**Vấn đề:** Check RM3 (`check_RM3_punctuation`) luôn trả về `False` cho mọi sample.
**Nguyên nhân:** Regex split `[.!?]` bị nhầm ở số thập phân/version (vd: `122.0a1`) và markdown header.
**Fix:**
- Bỏ qua số thứ tự đầu dòng (`1.`, `2.`)
- Bảo vệ số thập phân trước khi split câu
- Bỏ qua URL trong quá trình split
**File fix:** `ctqrs_scorer_v2_fixed.py`

### 3.5 CTQRS `max_possible` — Discrepancy 3 chiều (MS — Tuần 8)
**Phát hiện:** Ba giá trị khác nhau cho cùng một đại lượng:
| Nguồn | Giá trị |
|-------|---------|
| Code gốc GindeLab (`perfect_ctqrs.py`) | 16 (hardcode) |
| Paper E02/E12 mô tả | 17 |
| Tính lại từ trọng số thực tế 13 sub-check | **18** |

**Tính lại từ code:**
- RM1–RM4: 1 điểm mỗi check → 4
- RR1, RR2, RR4, RR5: 1 điểm mỗi check → 4
- RR3: 2 điểm → 2
- RA1–RA4: 2 điểm mỗi check → 8
- **Tổng = 18**

**Quyết định nhóm:** Dùng `max_possible=18` — giá trị duy nhất có thể chứng minh step-by-step từ code thực.
**Phân phối score thực tế (N=262):**

| Score | % | Số samples |
|-------|---|------------|
| 9 | 50.00% | 1 |
| 12 | 66.67% | 5 |
| 13 | 72.22% | 6 |
| 14 | 77.78% | 28 |
| 15 | 83.33% | 65 |
| 16 | 88.89% | 89 |
| 17 | 94.44% | 55 |
| 18 | 100.00% | 13 |

Max score đạt được là 18/18 = 100% (13 samples). Không có sample nào vượt 100%.
**Documented tại:** `proposal.md` §7.3 Threat 3 (Construct Validity).

### 3.6 SBERT thấp bất thường (MS — Debug 4-5)
**Phát hiện:** SBERT median = 0.632 — thấp hơn ngưỡng 0.82 rõ rệt.
**Nguyên nhân (Debug 4-5):**
- Qwen output dài hơn ground truth trung bình **1.82 lần**
- Qwen viết đầy đủ câu, có header markdown (`####`), bullet point chi tiết
- Ground truth Bugzilla có văn phong cô đọng, kỹ thuật, không có header
- SBERT `paraphrase-MiniLM-L6-v2` nhạy cảm với sự khác biệt văn phong/style, không chỉ nội dung ngữ nghĩa
**Kết luận:** SBERT thấp phản ánh **style mismatch**, không phải nội dung sai. Ghi nhận trong §5 Discussion paper.

---

## 4. Thống kê độ dài (Debug 5)

| | Ground Truth | Qwen Output |
|-|--------------|-------------|
| Mean (từ) | ~80 | ~146 |
| Tỷ lệ Qwen/GT | — | **1.82x** |

---

## 5. Thời gian chạy

| Giai đoạn | N | Thời gian | Tốc độ |
|-----------|---|-----------|--------|
| Pilot | 80 | 47.4 phút | ~0.59 phút/sample |
| Full run | 262 | ~2.6 giờ | ~0.59 phút/sample |
| **Tổng GPU T4** | 262 | **~3.4 giờ** | — |

---

## 6. Chi phí

| Mục | Chi phí |
|-----|---------|
| Kaggle GPU T4 (free tier, 30h/tuần) | $0 |
| HuggingFace model download (~15.2GB) | $0 |
| **Tổng** | **$0** |

---

## 7. File output đã tạo

| File | Mô tả | Owner |
|------|-------|-------|
| `pilot_llm_output.csv` | Output LLM pilot, N=80, 0 null | LR |
| `full_llm_output.csv` | Output LLM full run, N=262, 0 null | LR |
| `full_metrics_output_FINAL.csv` | Metrics đầy đủ (CTQRS/ROUGE/SBERT), N=262 | MS |
| `ctqrs_scorer_v2_fixed.py` | CTQRS scorer đã fix word-list + RM3 + max=18 | MS |
| `compute_metrics_MS.py` | Script tính metric gốc | MS |
| `debug_metrics.py` | Debug script (word-list, SBERT, length) | MS |
| `figure1_boxplot.png` | Boxplot phân phối 3 metrics | RW |
| `figure2_distribution.png` | Distribution plot | RW |
| `RQ1_results_FINAL.md` | Kết quả Wilcoxon + Cliff's δ cuối cùng | MS |
| `summary.csv` | 1 dòng/metric: tất cả số liệu thống kê | MS |
| `cost_log_LR.md` | Log GPU, thời gian, chi phí | LR |

---

## 8. Quyết định không thực hiện (và lý do)

| Hạng mục | Lý do không thực hiện |
|----------|----------------------|
| Fine-tuning Qwen | Ngoài scope RQ — RQ1 chỉ test few-shot |
| Paired test với GPT-4o | Thiếu per-instance GPT-4o data (E05 cũng ghi nhận hạn chế này) |
| Thay đổi threshold sau khi thấy data | Vi phạm nguyên tắc RBL-4 — không được HARKing |
| Dùng `max_possible=16` (code gốc) | Không khớp với trọng số thực → dùng 18 |

---

*Ghi chú cuối: Mọi thay đổi kỹ thuật đều phát sinh trong quá trình pilot/full run và được ghi lại tại đây. Không có thay đổi nào về RQ, metric, hay threshold sau khi GV phê duyệt proposal.*
