# Dataset — data/raw/README.md

## Thông tin nguồn

| Thuộc tính | Giá trị |
|------------|---------|
| **Tên dataset** | GindeLab/Ease_2025_AI_model — Bugzilla Bug Report Quality Dataset |
| **Nguồn** | https://github.com/GindeLab/Ease_2025_AI_model |
| **File gốc** | `Preprocess/Plus14_filtered_bug_report_scores_Summary.xlsx` |
| **Paper gốc** | Acharya & Ginde (2025), *Can We Enhance Bug Report Quality Using LLMs?*, EASE 2025 |
| **DOI paper** | https://dl.acm.org/doi/10.1145/3756681.3756995 |
| **License** | Public research dataset — xem repo GindeLab |
| **Ngày tải** | 2026-06-18 |
| **Tải bởi** | DG (Huỳnh Kha Thanh Hoàng, SE193944) |

---

## Thống kê

| | Giá trị |
|-|---------|
| Tổng dòng (sau lọc của tác giả E02) | **3,966** |
| Tổng cột | **32** |
| Domain | Bugzilla / Mozilla Firefox |
| Null (cột dùng trong experiment) | 0 |

---

## Cột quan trọng

| Cột | Vai trò | Ghi chú |
|-----|---------|---------|
| `text` | **Ground truth** — structured bug report gốc | ✅ Dùng cho ROUGE-1 và SBERT |
| `NEW_llama_output` | **Input** — unstructured summary (Llama3) | ✅ Input cho Qwen 3-shot |
| `total_score` | CTQRS score tuyệt đối (GindeLab, max=16) | Tham khảo |
| `score_percentage` | CTQRS % theo code gốc (max=16) | Tham khảo |
| `RM1`–`RA4` (_passed/_score) | 13 sub-check CTQRS | Tham khảo |

> **Quan trọng:** `max_possible` trong file gốc = 16. Nhóm tính lại từ trọng số thực = **18**. Xem `notes.md` §3.5.

---

## Split

| Split | Tỉ lệ | N | random_state |
|-------|-------|---|---|
| Train | 80% | 3,172 | 42 |
| Validation | 10% | 397 | 42 |
| **Test (dùng cho RQ1)** | **10%** | **262 valid** | **42** |

N=262 sau khi filter output hợp lệ (xem `notes.md` §2.2).

---

## Về Ground Truth — Không có annotation thủ công

Dataset có sẵn ground truth trong cột `text`. Nhóm **không annotate thủ công** — đúng như `proposal.md` §8.1:
> *"Ground truth: Có sẵn trong cột `text` của dataset — không cần annotation thủ công mới"*

Vì vậy không có `pilot_ground_truth.csv` / `full_ground_truth.csv` riêng.

---

## Reproduce split

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_excel('Plus14_filtered_bug_report_scores_Summary.xlsx')
_, test = train_test_split(df, test_size=0.1, random_state=42)
# Input:        test['NEW_llama_output']
# Ground truth: test['text']
```
