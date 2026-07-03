# Research Proposal: Đánh giá hiệu quả Qwen2.5-7B Few-shot so với Ngưỡng GPT-4o Few-shot trong Đánh giá Chất lượng Bug Report theo CTQRS

**Nhóm:** 3
**Thành viên:** 
Phan Hoàng Thông SE194047 — PL,
Huỳnh Kha Thanh Hoàng SE193944 — DG,
Nguyễn Công Huy SE192333 — LR,
Lại Minh Dũng SE194215 — MS,
Võ Thanh Phong SE194101 — RW.
**Ngày nộp:** 2026-06-20
**Version:** 1.0
**Trạng thái:** Đang chờ phê duyệt

---

## 2. Research Problem Statement

### 2.1 Bối cảnh & Tầm quan trọng

Bug report là nguồn thông tin chính để developer xác định, ưu tiên và xử lý lỗi phần mềm, nhưng chất lượng bug report do người dùng/tester viết thường không đồng đều — báo cáo thiếu hoặc mô tả mơ hồ về Steps to Reproduce (S2R), Expected Behavior (EB), hay Actual Behavior (AB) có thể khiến quá trình triage và sửa lỗi bị kéo dài đáng kể, đòi hỏi nhiều công trao đổi qua lại giữa developer và người báo lỗi. Việc tự động đánh giá và cải thiện chất lượng bug report bằng LLM đang được nhiều nghiên cứu khai thác, với CTQRS (Crowdsourced Test Report Quality Score) là một trong các metric được dùng phổ biến để đo lường khía cạnh này.

### 2.2 State of the Art

Acharya & Ginde (2025) — gọi tắt E02 trong bảng evidence của nhóm — fine-tune ba mô hình mã nguồn mở (Qwen2.5-7B, Mistral-7B, Llama3.2-3B) trên dataset Bugzilla và so sánh với GPT-4o ở chế độ 3-shot prompting, cho kết quả Qwen2.5-7B fine-tuned đạt CTQRS=77% so với GPT-4o 3-shot CTQRS=75%. Choi & Yang (2025) — E05 — xây dựng AgentReport, một pipeline multi-agent dùng Qwen2.5-7B với QLoRA-4bit và CTQRS prompting, đạt CTQRS=80.5% trong cấu hình đầy đủ; ablation của E05 cho thấy việc bỏ QLoRA khiến CTQRS giảm mạnh nhất, ngụ ý fine-tuning đóng vai trò quan trọng trong hiệu quả của Qwen. Yang (2025) — E12 — dùng PPO reinforcement learning với CTQRS làm reward signal trên Qwen2.5-7B, cải thiện CTQRS từ 0.46 lên 0.76. Cả ba nghiên cứu này đều tập trung vào việc *fine-tune* hoặc *huấn luyện thêm* Qwen2.5-7B để đạt hiệu quả cao, nhưng không nghiên cứu nào kiểm tra Qwen2.5-7B ở chế độ few-shot prompting thuần (không qua bất kỳ huấn luyện bổ sung) để xem liệu nó có tiếp cận được mức hiệu quả mà GPT-4o few-shot đã đạt được hay không.

### 2.3 GAP

**Loại GAP-T (Tool/LLM), N=13/13 paper trong evidence table đã kiểm tra.**

Mặc dù các nghiên cứu gần đây đã khám phá cả LLM mã nguồn mở (Qwen2.5-7B fine-tuned) lẫn LLM thương mại (GPT-4o few-shot) cho task đánh giá và cải thiện chất lượng bug report, chưa có nghiên cứu nào kiểm tra liệu Qwen2.5-7B ở chế độ few-shot (không fine-tune) có đạt được mức hiệu quả mà GPT-4o few-shot đã công bố hay không. Do đó, chưa rõ liệu open-source LLM ở điều kiện prompting tối giản (không cần fine-tuning) có thể tiếp cận hiệu quả của proprietary LLM hay không.

Phản chứng đã thực hiện qua bảng kiểm tra thủ công 13/13 paper (xem `SLR/gap-analysis.md`) và xác nhận độc lập qua tra cứu Elicit.com — không phát hiện công trình nào trong hoặc ngoài evidence table chạy Qwen2.5-7B ở chế độ few-shot để so sánh trực tiếp với GPT-4o few-shot trên cùng task.

### 2.4 Motivation

Nếu không trả lời được câu hỏi này, các nhóm phát triển/tổ chức với ngân sách hạn chế (không đủ tài nguyên GPU để fine-tune, hoặc không muốn đầu tư công sức huấn luyện) sẽ không có cơ sở thực nghiệm để quyết định liệu dùng Qwen2.5-7B ở chế độ few-shot đơn giản đã đủ để đạt chất lượng tương đương GPT-4o hay nhất thiết phải đầu tư fine-tuning — dẫn đến lựa chọn công cụ kém hiệu quả về chi phí.

---

## 3. Related Work

### 3.1 Overview

| Paper | Tool/LLM | Dataset (size) | Metric | Best result | Hạn chế chính |
|-------|----------|-----------------|--------|-------------|----------------|
| E01 Bo et al. 2024 (ChatBR) | BERT detector + GPT-3.5-turbo | 6 OSS projects (87 reports) | Precision, Recall, F1, Word2Vec similarity | Precision +25.38–29.20% vs SOTA | External validity: 6 dự án cụ thể |
| E02 Acharya & Ginde 2025 | Qwen2.5-7B/Mistral/Llama3.2 fine-tuned vs GPT-4o | Bugzilla (3,903) | CTQRS, ROUGE-1, SBERT | Qwen FT: CTQRS=77% vs GPT-4o 3-shot=75% | Fine-tuned trên Mozilla — external validity hạn chế |
| E03 Akyol et al. 2026 (ImproBR) | DistilBERT + GPT-4o mini + RAG | Mojira/Minecraft (139 targeted, 37 cho RQ2) | BEE tool, TF-IDF/Word2Vec cosine, Wilcoxon | Complete reports 7.9%→96.4% | Single domain; RQ2 sample nhỏ (37) |
| E05 Choi & Yang 2025 (AgentReport) | Qwen2.5-7B + QLoRA-4bit | Bugzilla (3,966) | CTQRS, ROUGE-1, SBERT | Full pipeline: CTQRS=80.5% | Paired significance testing không khả thi (thiếu per-instance baseline) |
| E12 Yang 2025 (CTQRS-RL) | Qwen2.5-7B + PPO RL | Bugzilla (3,966) | CTQRS, SBERT, ROUGE-1 | CTQRS 0.46→0.76 | Chỉ train/test trên report chất lượng cao |
| E14 Dinç et al. 2025 | RoBERTa, GPT Judge LLM, RAG | Mozilla Firefox (10,000) | F1-score | RoBERTa F1=0.909 (tốt nhất) | LLM kém hơn fine-tuned RoBERTa; chỉ Firefox |

*(Bảng trên trích 6/13 paper liên quan trực tiếp nhất đến GAP-T; toàn bộ 13 paper xem `SLR/evidence-table-merged.md`)*

### 3.2 Pattern Analysis

Nhìn chung, các nghiên cứu dùng Qwen2.5-7B cho task này đều áp dụng một hình thức huấn luyện bổ sung (fine-tuning LoRA/QLoRA hoặc reinforcement learning) trước khi đo CTQRS — thể hiện qua E02, E05, E12. Không có nghiên cứu nào trong nhóm sử dụng Qwen2.5-7B kiểm tra hiệu quả ở chế độ few-shot/zero-shot thuần.

Nhìn chung, GPT-4o (hoặc các biến thể mini) luôn xuất hiện ở vai trò baseline few-shot/zero-shot, không qua fine-tuning — thể hiện qua E02 (3-shot), E03 (GPT-4o mini few-shot), E07 (GPT-4o-mini Direct/Agentic-LLM) — cho thấy việc fine-tune GPT-4o ít được khai thác trong literature hiện tại, một phần do giới hạn chi phí và (gần đây) chính sách wind-down nền tảng fine-tuning của OpenAI.

Nhìn chung, CTQRS là metric được 4/13 paper sử dụng (E02, E05, E09 gián tiếp qua OB/EB/S2R, E12), toàn bộ trên nền Bugzilla/Mozilla — phản ánh GAP-M về việc thiếu validation cross-domain.

Nhìn chung, vấn đề thiếu dữ liệu paired khi so sánh với baseline đã công bố sẵn (không tự chạy lại) là hạn chế được chính literature ghi nhận — thể hiện qua phát biểu của E05 rằng "paired significance testing not feasible due to unavailability of per-instance baseline results", củng cố cho lựa chọn phương pháp absolute-threshold testing trong thiết kế của nhóm.

### 3.3 GAP Mapping

| GAP | Evidence (số paper support) | Status |
|-----|------------------------------|--------|
| GAP-T | 13/13 paper kiểm tra; không paper nào chạy Qwen few-shot so với GPT-4o few-shot cùng điều kiện | Confirmed |
| GAP-M | 4/13 paper dùng CTQRS (E02, E05, E09, E12), toàn bộ trên Bugzilla/Mozilla | Confirmed-Deferred (address một phần qua RQ2 cross-domain Mojira) |

---

## 4. Research Questions

> Chốt tại đây. Sau khi GV phê duyệt, không được thay đổi RQ, metric, hay threshold.

### RQ1

**RQ1:** Trên ≈397 bug reports từ Bugzilla (GindeLab/Ease_2025_AI_model, tự split 80/10/10 từ N=3,966) [P], Qwen2.5-7B-Instruct với 3-shot prompting (Alpaca-LoRA template, temperature tối thiểu cho phép, do mô hình yêu cầu >0) [I] có đạt CTQRS ≥ 75%, SBERT ≥ 0.82, ROUGE-1 ≥ 0.47 [O] — các ngưỡng đã công bố cho GPT-4o 3-shot trong E02 Figure 4 [C] không?

**Loại claim:** Absolute threshold (không phải comparative — không tự chạy lại GPT-4o; không có dữ liệu paired giữa hai model).

**Ghi chú thuật ngữ:** "3-shot" nghĩa là prompt đưa kèm 3 cặp ví dụ mẫu (input-output) trước khi yêu cầu model xử lý input thật — đây là điều kiện prompting cố định, áp dụng giống nhau khi đo cả Qwen2.5-7B (thực nghiệm này) và khi E02 đo GPT-4o (threshold tham chiếu), nhằm đảm bảo so sánh cùng điều kiện few-shot.

**H0 (CTQRS):** Qwen2.5-7B 3-shot KHÔNG đạt CTQRS ≥ 75% (median trên ≈397 samples).
**H1 (CTQRS):** Qwen2.5-7B 3-shot ĐẠT CTQRS ≥ 75%.
**Metric:** CTQRS (CTQRS scorer, GindeLab repo, max_possible=16)
**Threshold:** 75% (Case 1 — E02, Figure 4, nhóm "3 Shot ChatGPT")
**Statistical test:** Wilcoxon signed-rank one-sample test (α = 0.05)

**H0 (SBERT):** Qwen2.5-7B 3-shot KHÔNG đạt SBERT ≥ 0.82.
**H1 (SBERT):** Qwen2.5-7B 3-shot ĐẠT SBERT ≥ 0.82.
**Metric:** SBERT cosine similarity (sentence-transformers, model `paraphrase-MiniLM-L6-v2`)
**Threshold:** 0.82 (Case 1 — E02, Figure 4)
**Statistical test:** Wilcoxon signed-rank one-sample test (α = 0.05)

**H0 (ROUGE-1):** Qwen2.5-7B 3-shot KHÔNG đạt ROUGE-1 F1 ≥ 0.47.
**H1 (ROUGE-1):** Qwen2.5-7B 3-shot ĐẠT ROUGE-1 F1 ≥ 0.47.
**Metric:** ROUGE-1 F1 (rouge-score 0.4.x)
**Threshold:** 0.47 (Case 1 — E02, Figure 4)
**Statistical test:** Wilcoxon signed-rank one-sample test (α = 0.05)

### RQ2

**RQ2:** Trên 37 bug reports từ Mojira/Minecraft (E03, Akyol et al. 2026) [P], Qwen2.5-7B-Instruct 3-shot [I] có duy trì CTQRS với độ sụt giảm ≤ 10pp so với kết quả trên Bugzilla [O] không — tức CTQRS metric có generalizable sang domain mới [C]?

**Loại claim:** Absolute threshold (so sánh độ sụt giảm Δ với ngưỡng cố định).

**H0:** Qwen2.5-7B 3-shot KHÔNG duy trì CTQRS với Δ ≤ 10pp khi chuyển từ Bugzilla sang Mojira (Δ > 10pp).
**H1:** Qwen2.5-7B 3-shot DUY TRÌ CTQRS với Δ ≤ 10pp (Δ ≤ 10pp).
**Metric:** CTQRS
**Threshold:** Δ ≤ 10pp (Case 2 — floor từ E02 Figure 4 "FT models Cross Project": 77%→70%, Δ=7pp, làm tròn lên 10pp)
**Statistical test:** Mann-Whitney U (α = 0.05) — so sánh 2 nhóm điểm số độc lập (Bugzilla test set vs Mojira subset)

---

## 5. Experiment Protocol

### 5.1 Pipeline

**Base paper:** E02 Acharya & Ginde 2025 (duy nhất trong 13 paper có cả Qwen2.5-7B và GPT-4o trên cùng dataset Bugzilla với CTQRS).

**Bước 1 — Chuẩn bị dữ liệu:**
- Nguồn: `GindeLab/Ease_2025_AI_model/Preprocess/Plus14_filtered_bug_report_scores_Summary.xlsx` (N=3,966 dòng, đã xác nhận tải và đọc được)
- Cột input: `NEW_llama_output` (unstructured summary, sinh bởi Llama3)
- Cột ground truth: `text` (structured bug report gốc)
- Split 80/10/10 (train≈3,172 / test≈397 / validation≈397) với `random_state` cố định do nhóm tự quy định (E02 không công bố seed)

**Bước 2 — Inference Qwen2.5-7B 3-shot:**
- Model: `unsloth/Qwen2.5-7B-Instruct` (HuggingFace)
- Môi trường: Kaggle Notebook, GPU T4 x2, Internet ON
- Cấu hình: `temperature=0.01` (giá trị tối thiểu, do Qwen yêu cầu >0), `do_sample=False`, `max_new_tokens=512`
- Prompt: Alpaca-LoRA template nguyên văn theo E02 Listing 2, kèm 3 exemplar pairs lấy từ phần training set (xem định nghĩa "3-shot" tại §4)
- Output: JSON có cấu trúc S2R / Expected Result / Actual Result / Additional Information

**Bước 3 — Tính metric:**
- CTQRS: scorer từ `GindeLab/Ease_2025_AI_model/Evaluation/` (Stanza NLP, 13 sub-checks, `max_possible=16` — lưu ý khác với mô tả paper ghi max=17, ghi rõ discrepancy khi báo cáo %)
- ROUGE-1 F1: `rouge-score` 0.4.x, key `rouge1`
- SBERT: `sentence-transformers`, model `paraphrase-MiniLM-L6-v2`, cosine similarity giữa output Qwen và cột `text` ground truth

**Bước 4 — Cross-domain (RQ2):**
- Chạy lại đúng pipeline Bước 2-3 trên 37 Mojira ground-truth pairs (E03, Akyol et al. 2026)
- Không re-train, không thay đổi prompt

**Bước 5 — Statistical testing:**
- RQ1: Wilcoxon signed-rank one-sample test cho mỗi metric (CTQRS, SBERT, ROUGE-1) — so median của ≈397 điểm số Qwen với từng threshold
- RQ2: Mann-Whitney U so sánh phân phối CTQRS giữa Bugzilla test set và Mojira subset

### 5.2 Dataset

| Thuộc tính | Giá trị |
|------------|---------|
| Nguồn | `github.com/GindeLab/Ease_2025_AI_model/Preprocess/Plus14_filtered_bug_report_scores_Summary.xlsx` |
| N tổng | 3,966 |
| N test (sau split) | ≈397 |
| N cross-domain (Mojira) | 37 (từ E03) |
| Trạng thái accessible | ✅ Đã tải và đọc thử thành công (xác nhận 3,966 dòng, 32 cột, không có giá trị null ở cột input) |

### 5.3 LLM Configuration

| Thông số | Giá trị |
|----------|---------|
| Model (thực nghiệm) | `unsloth/Qwen2.5-7B-Instruct` |
| Model (threshold tham chiếu) | GPT-4o 3-shot — **version cụ thể KHÔNG được công bố trong paper E02** (xem Threat mới tại §7.1) |
| Nền tảng | HuggingFace Transformers, chạy trên Kaggle GPU T4 x2 |
| Temperature | 0.01 (tối thiểu cho phép) |
| Sampling | `do_sample=False` (deterministic) |
| Max new tokens | 512 |
| Prompt strategy | 3-shot, Alpaca-LoRA template (E02 Listing 2) |

### 5.4 Measurement

| Metric | Thư viện/version | Tính trên |
|--------|-------------------|-----------|
| CTQRS | GindeLab CTQRS scorer (Stanza NLP), max_possible=16 | Output Qwen |
| ROUGE-1 F1 | rouge-score 0.4.x | Output Qwen vs cột `text` |
| SBERT cosine | sentence-transformers, paraphrase-MiniLM-L6-v2 | Output Qwen vs cột `text` |

### 5.5 Statistical Plan

| RQ | Test | α | Effect size |
|----|------|---|-------------|
| RQ1 (×3 metric) | Wilcoxon signed-rank one-sample | 0.05 | — |
| RQ2 | Mann-Whitney U | 0.05 | Cliff's δ |

---

## 6. Evaluation Plan

### 6.1 Bảng tiêu chí đánh giá

| RQ | Metric | Ngưỡng | Test | H0 bị reject khi... | Kết quả âm tính có ý nghĩa? |
|----|--------|--------|------|----------------------|-------------------------------|
| RQ1 | CTQRS | ≥75% | Wilcoxon one-sample | p<0.05 và median ≥75% | Có — cho biết few-shot chưa đủ, cần fine-tuning |
| RQ1 | SBERT | ≥0.82 | Wilcoxon one-sample | p<0.05 và median ≥0.82 | Có — tương tự trên |
| RQ1 | ROUGE-1 | ≥0.47 | Wilcoxon one-sample | p<0.05 và median ≥0.47 | Có — tương tự trên |
| RQ2 | CTQRS Δ | ≤10pp | Mann-Whitney U | p≥0.05 (không khác biệt có ý nghĩa) | Có — nếu Δ>10pp, CTQRS không generalize tốt sang Mojira |

### 6.2 Diễn giải tổ hợp kết quả

- **Double positive** (cả 3 metric RQ1 đạt ngưỡng): Qwen2.5-7B few-shot tiếp cận được hiệu quả GPT-4o few-shot mà không cần fine-tuning — kết luận mạnh, khuyến nghị dùng few-shot cho ngân sách hạn chế.
- **Mixed** (một số metric đạt, một số không — ví dụ CTQRS đạt nhưng ROUGE không đạt): Qwen few-shot có ưu thế ở khía cạnh ngữ nghĩa/cấu trúc (CTQRS, SBERT) nhưng kém ở khía cạnh từ vựng (ROUGE) — gợi ý cần fine-tuning nếu ưu tiên overlap từ vựng với ground truth.
- **Double negative** (không metric nào đạt ngưỡng): Few-shot không đủ; fine-tuning (như E02, E05, E12 đã làm) là cần thiết để Qwen tiếp cận hiệu quả GPT-4o — kết quả vẫn có giá trị báo cáo, hướng dẫn phân bổ tài nguyên (không nên chỉ dùng few-shot nếu cần chất lượng cao).

### 6.3 Sub-group analysis (nếu có)

Không có kế hoạch sub-group analysis tại thời điểm proposal (n_group cho mỗi nhóm con dưới 30 sẽ không đủ power thống kê với cỡ mẫu hiện tại ≈397). Nếu pilot Tuần 7 cho thấy cần thiết (ví dụ phân tích theo độ dài input report), sẽ đề xuất qua quy trình Amendment.

---

## 7. Threats to Validity

### 7.1 Internal Validity

**Threat 1:** Model Qwen2.5-7B trên HuggingFace có thể được cập nhật version ngầm giữa lúc setup và lúc chạy full experiment, ảnh hưởng đến reproducibility.
**Mitigation:** Pin version cụ thể của model checkpoint (ghi rõ commit hash/revision của `unsloth/Qwen2.5-7B-Instruct` tại thời điểm tải), log lại trong `results/full_llm_output.csv` metadata.

**Threat 2:** Temperature=0.01 (không phải 0 tuyệt đối, do giới hạn API của Qwen) có thể gây dao động nhỏ giữa các lần chạy.
**Mitigation:** Cố định `do_sample=False` để đảm bảo decoding deterministic (greedy), giảm thiểu ảnh hưởng của temperature; ghi rõ seed nếu framework yêu cầu.

**Threat 3 (mới):** Paper E02 không công bố version cụ thể của GPT-4o đã dùng để tạo ra threshold tham chiếu (75%/0.82/0.47) — toàn văn chỉ ghi "ChatGPT"/"GPT-4o" mà không kèm ngày phát hành/version string (kiểu `gpt-4o-2024-08-06`). Đáng chú ý, trích dẫn tham khảo [53] trong E02 ghi rõ là "ChatGPT (Version 3.5)", trong khi phần kết quả (Figure 4) lại báo cáo là "ChatGPT 4o" — cho thấy có sự không nhất quán trong cách trích dẫn model của chính paper gốc.
**Mitigation:** Đây là hạn chế vốn có của paper gốc, nhóm không thể tự suy diễn version cụ thể không được công bố. Ghi rõ giới hạn này khi diễn giải threshold (không khẳng định threshold 75% tương ứng với một phiên bản GPT-4o cụ thể, ổn định theo thời gian). Nếu nhóm tự chạy thêm GPT-4o trong các bước nghiên cứu tiếp theo, sẽ pin version cụ thể (ví dụ `gpt-4o-2024-08-06`) và log lại đầy đủ.

### 7.2 External Validity

**Threat 1:** Test set chỉ giới hạn trong domain Bugzilla/Mozilla (RQ1) — kết quả có thể không generalize sang domain khác ngoài Mojira (đã test ở RQ2).
**Mitigation:** RQ2 bổ sung một domain khác (Mojira/Minecraft) để kiểm tra một phần generalizability; ghi rõ trong Conclusion rằng kết luận chỉ áp dụng cho 2 domain đã test.

**Threat 2:** Cỡ mẫu cross-domain (Mojira, N=37) nhỏ — đã được chính E03 (Akyol et al. 2026) tự ghi nhận là hạn chế của paper gốc.
**Mitigation:** Không mở rộng N vượt quá dữ liệu ground-truth có sẵn từ E03; báo cáo rõ cỡ mẫu nhỏ trong Conclusion, tránh overclaim.

### 7.3 Construct Validity

**Threat 1:** Test set ≈397 samples tự split từ N=3,966 không đảm bảo trùng khớp với test set 391 mà E02 dùng để sinh ra threshold tham chiếu (E02 dùng N=3,903 sau bước lọc SBERT bổ sung mà nhóm chưa áp dụng; random seed không công bố).
**Mitigation:** Ghi rõ trong Conclusion rằng threshold 75%/0.82/0.47 chỉ mang tính tham chiếu lịch sử (Case 1), không phải kết quả thực nghiệm trên cùng dữ liệu paired; không diễn giải kết luận "đạt/không đạt ngưỡng" như một so sánh trực tiếp công bằng tuyệt đối.

**Threat 2:** Không thể thực hiện paired significance test giữa Qwen và GPT-4o do thiếu per-instance baseline của GPT-4o.
**Mitigation:** Đây là hạn chế đã được ghi nhận trong literature (E05 — Choi & Yang 2025 — tự thừa nhận "paired significance testing not feasible due to unavailability of per-instance baseline results"); nhóm dùng one-sample test thay thế, ghi rõ giới hạn này trong Conclusion.

**Threat 3:** CTQRS có `max_possible=16` trong code thực tế của GindeLab nhưng paper E02/E12 mô tả max=17 — discrepancy giữa văn bản và implementation.
**Mitigation:** Dùng `max_possible=16` theo code thực tế (vì đây là công cụ thật sẽ chạy), ghi rõ discrepancy này khi báo cáo % trong RBL-4/RBL-5.

### 7.4 Conclusion Validity

**Threat 1:** Cỡ mẫu RQ2 (N=37) có thể không đủ power thống kê cho Mann-Whitney U để phát hiện sự khác biệt thực sự nếu có.
**Mitigation:** Báo cáo effect size (Cliff's δ) song song với p-value để đánh giá độ lớn thực tế của sự khác biệt, không chỉ dựa vào significance.

**Threat 2:** Thực hiện 3 statistical test riêng biệt cho RQ1 (CTQRS, SBERT, ROUGE-1) làm tăng nguy cơ Type I error (multiple testing).
**Mitigation:** Áp dụng hiệu chỉnh Bonferroni nếu cần diễn giải kết hợp cả 3 test như một kết luận tổng thể (α_adjusted = 0.05/3 ≈ 0.017); báo cáo cả p-value gốc và đã hiệu chỉnh.

---

## 8. Timeline & Resources

### 8.0 Phân công vai trò

| Role | Thành viên | Trách nhiệm trong experiment |
|------|------------|-------------------------------|
| PL | Phan Hoàng Thông | Coordinate tiến độ, review nhất quán toàn proposal, viết §2 + §4, nộp GV |
| DG | Huỳnh Kha Thanh Hoàng | Viết §3 Related Work, quản lý dataset, viết script split 80/10/10, ground truth annotation |
| LR | Nguyễn Công Huy | Setup Qwen2.5-7B trên Kaggle, viết + chạy script batch inference, log output |
| MS | Lại Minh Dũng | Implement CTQRS/ROUGE/SBERT scorer, chạy statistical test, tính effect size |
| RW | Võ Thanh Phong | Viết §1, §7; proofread toàn bộ; tạo figures; làm slide bảo vệ đề cương |

### 8.1 Resource Inventory

| Tài nguyên | Trạng thái | Owner | Ghi chú |
|------------|------------|-------|---------|
| Dataset | ✅ | DG | `Plus14_filtered_bug_report_scores_Summary.xlsx` — đã tải và đọc thử thành công, N=3,966 |
| Model | ✅ | LR | `unsloth/Qwen2.5-7B-Instruct` — HuggingFace, free, đã xác nhận load được |
| Compute | ✅ | LR | Kaggle Notebook, GPU T4 x2, 30h/tuần free tier |
| Ground truth | ✅ | DG | Có sẵn trong cột `text` của dataset — không cần annotation thủ công mới |

### 8.2 Chi phí ước tính

| Item | Số lượng | Đơn giá | Tổng |
|------|----------|---------|------|
| Kaggle GPU (T4 x2) | ~3-5 giờ (pilot + full run) | $0 (free tier 30h/tuần) | $0 |
| HuggingFace model download | 1 lần (~15GB) | $0 | $0 |
| **Tổng chi phí dự kiến** | | | **$0** |

### 8.3 Timeline chi tiết (Tuần 5-10)

> **Tuần 5-6:** Song song viết proposal + chuẩn bị tài nguyên
> **Tuần 7-8:** Thực nghiệm — xem chi tiết RBL-4
> **Tuần 9-10:** Viết paper + present — xem RBL-5

| Tuần | Hoạt động | Owner | Checkpoint — output cụ thể |
|------|-----------|-------|------------------------------|
| 5 | Viết proposal §2-§7 | PL + DG + RW | Draft §2-§7 trong `proposal.md` |
| 5 | Viết script split 80/10/10 + verify dataset | DG | `data/raw/` + `data/test_split.csv` + README |
| 5 | Setup Qwen2.5-7B trên Kaggle, test 1 sample | LR | Notebook chạy được, output mẫu in ra màn hình |
| 5 | Implement CTQRS/ROUGE/SBERT scorer | MS | `compute_metric.py` draft, test trên data giả |
| 5 | Draft §7 Threats to Validity | RW | Draft §7 trong `proposal.md` |
| 6 | Hoàn thiện §1, §8 + ghép toàn bộ `proposal.md` v1.0 | PL | `proposal.md` v1.0 — nộp GV |
| 6 | ★ **GV phê duyệt** (hard deadline: cuối Tuần 6) | PL | `proposal.md` → Trạng thái "Đã phê duyệt" |
| 7 | Chạy pilot (~40-80 samples) trên Qwen | LR | `results/pilot_llm_output.csv` |
| 7 | Tính metric pilot, kiểm tra phân phối | MS | `results/pilot_analysis.ipynb` |
| 7 | Họp review pilot — amendment nếu cần | Tất cả | Meeting note (PL ghi) |
| 8 | Chạy full batch ≈397 samples + 37 Mojira | LR | `results/full_llm_output.csv` + cost log |
| 8 | Tính metric toàn bộ + statistical tests | MS | `results/full_analysis.ipynb` |
| 8 | Tạo figures (≥2 plots: boxplot + distribution) | RW | `figures/` |
| 9-10 | Viết paper + present | Tất cả | Xem RBL-5 |

### 8.4 Contingency Plan

**Nếu proposal chưa duyệt cuối Tuần 6:** Chỉ làm RQ1, tạm hoãn RQ2 (cross-domain) — báo GV ngay.
**Nếu Kaggle GPU quota hết (30h/tuần):** Chia batch nhỏ, chạy qua nhiều ngày, hoặc dùng Colab T4 free làm phương án dự phòng.
**Nếu dataset GitHub không truy cập được:** File `Plus14_filtered_bug_report_scores_Summary.xlsx` đã được tải về và lưu cục bộ — không phụ thuộc vào uptime của GitHub trong quá trình chạy thực nghiệm.
**Nếu pilot Tuần 7 phát hiện vấn đề kỹ thuật** (ví dụ phân phối CTQRS không như kỳ vọng): Nộp Proposal Amendment trong 24 giờ sau pilot meeting, theo template `proposal-amendment-v1.1.md`.
**Nếu thành viên không kịp deadline:** PL escalate sau 48 giờ trễ; redistribute task cho thành viên khác.

### 8.5 Checkpoint per member (Tuần 5-10)

| Role | Tuần 5 | Tuần 6 | Tuần 7 | Tuần 8 |
|------|--------|--------|--------|--------|
| PL | Draft §2, §4 | Nộp proposal + theo dõi GV | Chủ trì pilot meeting | Verify full run |
| DG | `data/raw/` + README | Confirm §8.1 resource | `data/pilot_ground_truth.csv` (nếu cần) | Verify full data |
| LR | `test_qwen_inference.ipynb` chạy được | Confirm compute trong §8.1 | `results/pilot_llm_output.csv` | `results/full_llm_output.csv` |
| MS | `compute_metric.py` draft | Confirm stat test plan | `results/pilot_analysis.ipynb` | `results/full_analysis.ipynb` |
| RW | Draft §7 | Proofread toàn proposal | Hỗ trợ pilot meeting | `figures/` |

---

**Sau khi GV phê duyệt proposal:** Không được thay đổi RQ, metric, hay threshold. Mọi thay đổi kỹ thuật phát hiện trong pilot phải qua quy trình Amendment (xem RBL-3 §8.6).

**Bước tiếp theo:** Chạy thực nghiệm theo đúng protocol đã chốt trong §5.