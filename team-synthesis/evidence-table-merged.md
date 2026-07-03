# Evidence Table Merged

**Merged source:** Evidence tables from team members
**Deduplication rule:** If the same paper appears in multiple evidence tables, only one merged record is kept. The most detailed and verifiable extraction is retained.
**Main merged evidence:** N = 13 papers
**Cập nhật:** 2026-06-17 — bổ sung số liệu chi tiết cho E05, E06, E07, E09 (trước đó thiếu/N/A do extraction sót, không phải do paper không có)


---

# A. Main Merged Evidence

## Evidence 01

**Paper:** Bo et al. (2024), *ChatBR: Automated Assessment and Improvement of Bug Report Quality Using ChatGPT*, ASE.
**DOI / URL:** https://doi.org/10.1145/3691620.3695518

**Tool / LLM:** BERT fine-tuned detector + ChatGPT / GPT-3.5-turbo

**Dataset:** Song et al.'s annotated dataset; bug reports from six OSS projects: AspectJ, Birt, Eclipse, JDT, SWT, Tomcat

**Metric:** Precision, Accuracy, Recall, F1-score, Word2Vec semantic similarity, number of ChatGPT runs

**Result:**
Precision improved by 25.38%–29.20% compared with SOTA/BEE. Average semantic similarity was 77.62%. More than 99.9% of bug reports were completed within five ChatGPT runs.

**Limitations reported:**
Potential data leakage risk with ChatGPT was discussed and mitigated. External validity is limited because the evaluation used six specific OSS projects.

---

## Evidence 02

**Paper:** Acharya & Ginde (2025), *Can We Enhance Bug Report Quality Using LLMs?: An Empirical Study of LLM-Based Bug Report Generation*, EASE.
**DOI / URL:** https://dl.acm.org/doi/10.1145/3756681.3756995

**Tool / LLM:** Fine-tuned Qwen 2.5-7B, Mistral-7B, Llama 3.2-3B; ChatGPT-4o baseline; Llama3 for synthetic data generation

**Dataset:** Bugzilla; 15,000 fixed bug reports raw; 3,903 after filtering and synthetic pairing; 80/10/10 split; 4-fold cross-validation

**Metric:** CTQRS, ROUGE-1, SBERT, Accuracy, F1, METEOR, missing-information detection

**Result:**
Qwen 2.5 achieved CTQRS = 77%, ROUGE = 0.61, SBERT = 85%, compared with ChatGPT-4o 3-shot CTQRS = 75%, ROUGE = 0.47, SBERT = 82%. In cross-project generalization, Qwen 2.5 achieved CTQRS = 70%, ROUGE = 0.59, SBERT = 75%. For missing information detection, Qwen 2.5 achieved F1 S2R = 76%, AB = 45%, EB = 44%.

**Limitations reported:**
LLM hallucination, prompt sensitivity, external validity limitations because fine-tuning used Mozilla projects, and lexical metrics may underestimate semantic quality.

---

## Evidence 03

**Paper:** Akyol et al. (2026), *ImproBR: Bug Report Improver Using LLMs*, EASE 2026 / arXiv.
**URL:** https://arxiv.org/abs/2604.26142

**Tool / LLM:** DistilBERT fine-tuned detector, heuristic detector, GPT-4o mini, RAG with LangChain/Chroma/text-embedding-ada-002, Cross-Encoder ms-marco-MiniLM-L-6-v2, few-shot prompting

**Dataset:** Mojira / Minecraft bug tracker; 24,998 reports population; 996 stratified sample; targeted 139 reports; 37 ground-truth + raw duplicate pairs for RQ2

**Metric:** Structural completeness, executable S2R, reproducibility, TF-IDF cosine similarity, Word2Vec cosine similarity, Wilcoxon signed-rank, Cliff's δ, Cohen's Kappa

**Result:**
Complete reports improved from 7.9% to 96.4%. EB improved from 12.2% to 96.4%. S2R improved from 56.1% to 97.1%. Executable S2R improved from 28.8% to 67.6%. Reproducible reports improved from 0.7% to 9.4%. TF-IDF average improved from 9.6% to 29.3%. Word2Vec average improved from 34.7% to 77.1%.

**Limitations reported:**
Single domain dataset from Minecraft/Mojira; small RQ2 sample of 37 reports; results depend on GPT-4o mini; screenshots/video links were not processed; BEE tool is only a proxy for true report quality.

---

## Evidence 05

**Paper:** Choi & Yang (2025), *AgentReport: A Multi-Agent LLM Approach for Automated and Reproducible Bug Report Generation*, Applied Sciences.
**URL:** https://www.mdpi.com/2076-3417/15/22/11931

**Tool / LLM:** Qwen2.5-7B-Instruct, QLoRA-4bit, CTQRS prompting, Chain-of-Thought, one-shot exemplar

**Dataset:** 3,966 summary-report pairs from Bugzilla

**Metric:** CTQRS, ROUGE-1 Recall, ROUGE-1 F1, SBERT

**Result:**
Ablation study (Table 3) shows full AgentReport pipeline ("All combined") achieves CTQRS=80.5%, ROUGE-1 Recall=84.6%, ROUGE-1 F1=56.8%, SBERT=86.4%, compared with base configuration CTQRS=74.7%, ROUGE-1 Recall=65.6%, ROUGE-1 F1=24.1%, SBERT=83.0%. Best individual component: one-shot retrieval achieves highest CTQRS (80.0%) among single components; QLoRA-4bit only achieves highest SBERT (87.3%). Removing QLoRA causes largest CTQRS drop (76.9%), confirming fine-tuning is the most critical component.

**Limitations reported:**
Internal validity: single random seed and fixed data partitioning — sensitivity to distributional shifts unexplored; deterministic decoding (temperature=0) does not account for alternative sampling strategies. External validity: limited to Bugzilla only — not tested on GitHub Issues or Jira; cross-platform experiments not yet conducted; domain variations (mobile apps, enterprise systems, security reports) unverified. Construct validity: CTQRS may not capture rhetorical flow; ROUGE does not assess contextual appropriateness; SBERT varies by embedding model choice; **paired significance testing not feasible due to unavailability of per-instance baseline results**. Practical: adoption requires trust, workflow integration, and compatibility with issue trackers.

---

## Evidence 06

**Paper:** Mahmud et al. (2025), *Combining Language and App UI Analysis for the Automated Assessment of Bug Reproduction Steps*, ICPC'25.
**DOI / URL:** http://arxiv.org/abs/2502.04251

**Tool / LLM:** GPT-4 + app UI execution model (graph-based dynamic analysis) + GUI interaction mapping

**Dataset:** Development set: 54 bug reports from 31 Android apps; Test set: 21 bug reports from 6 Android apps (Euler dataset)

**Metric:** Precision, Recall, F1 (S2R quality annotation + missing S2R suggestion)

**Result:**
AstroBR outperforms baseline (Euler) by 25.2% in F1 for S2R quality annotation (overall F1=0.879 vs Euler F1=0.702). For missing S2R suggestion, AstroBR outperforms Euler by 71.4% in F1 (F1=0.639 vs Euler F1=0.373). Improvement is statistically significant (Wilcoxon p=0.03/0.004/0.005 for precision/recall/F1).

**Limitations reported:**
Small test set (21 reports from 6 Android apps); execution model completeness depends on CrashScope coverage; rotation interactions not supported; Android only; results may not generalize to other platforms.

---

## Evidence 07

**Paper:** Fahim et al. (2025), *Crash Report Enhancement with Large Language Models: An Empirical Study*.
**DOI / URL:** http://arxiv.org/abs/2509.13535

**Tool / LLM:** GPT-4o-mini, Direct-LLM, Agentic-LLM

**Dataset:** 492 real-world crash reports from 8 Java open-source systems

**Metric:** Top-1/Top-3/Top-5 localization accuracy, CodeBLEU, manual evaluation, LLM-as-a-judge, user study

**Result:**
Among 492 crash reports from 8 Java OSS systems, only 11.79% had Steps to Reproduce, 39.84% had Root-cause hypothesis, and 20.93% had Suggested fix (Table 2). LLM-enhanced crash reports substantially improve problem localization accuracy: Direct-LLM achieves average Top-1=40.24%, Agentic-LLM achieves Top-1=43.09%, compared with DevCR (developer-written) Top-1=10.57%, Top-3=17.28%, Top-5=22.97% (Table 3). Agentic-LLM consistently outperforms Direct-LLM across all 8 systems.

**Limitations reported:**
Internal validity: effectiveness depends on quality of inputs (stack traces, source code, developer-written reports) — incomplete or noisy inputs may affect generated report quality. External validity: limited to 492 crash reports from 8 Java OSS systems — may not generalize to other languages (C++, Python) or industrial systems; analysis focuses on crash reports with stack traces only — non-crash bug reports not evaluated. Construct validity: automated metrics (CodeBLEU, localization accuracy) may not cover every dimension of practical debugging; LLM-as-a-judge used to scale evaluation across all reports.

---

## Evidence 09

**Paper:** Pourasad et al. (2026), *FeedAIde: Guiding App Users to Submit Rich Feedback Reports by Asking Context-Aware Follow-Up Questions*, MOBILESoft.
**DOI / URL:** 10.1145/3795077.3795120

**Tool / LLM:** Multimodal LLM (GPT-4.1 via AIProxy/OpenAI), context-aware follow-up questions, iOS Swift Package

**Dataset:** 54 feedback reports from user testing on a gym iOS app (PPEmployee); 7 participants; 4 scenarios (2 bug reports + 2 feature requests)

**Metric:** User ratings (4-point scale: ease + helpfulness); expert assessment using OB, EB, S2R dimensions (3-point scale 0–2); Cohen's Kappa inter-rater

**Result:**
Bug report S2R score: Traditional=0.14/2 vs FeedAIde=2.00/2. Ease rating: 2.86→3.71/4 (+0.85). Helpfulness rating: 1.14→3.43/4 (+2.29). Feature request Description: 0%→100%. Correct summary: 69.2%→92.3%. Product version: 0%→100%. Inter-rater agreement: Cohen's Kappa κ=0.906 (bug reports), κ=0.921 (feature requests). All 7 participants preferred FeedAIde over traditional text field.

**Limitations reported:**
Small sample (7 participants, 1 app); observer bias risk; GPT-4.1 dependency — different models may produce different results; follow-up questions tend to focus on refining solutions rather than uncovering root causes; results not generalizable beyond single gym app context; loading times 10–20 seconds per request.

---

## Evidence 10

**Paper:** Chaves et al. (2025), *Automatic Generation of Bug Reports Using Large Language Models: An Evaluation in a Software Institute*, SBQS.
**URL:** https://sol.sbc.org.br/index.php/sbqs/article/view/39022

**Tool / LLM:** Fine-tuned T5 model

**Dataset:** Software institute test team; mobile device testing context; 8 testers; 5 bug types

**Metric:** Tester judgment: valid, partially valid, invalid; post-experiment survey

**Result:**
The T5-based system generates bug reports from brief descriptions. The paper reports that 3 of the 5 bug types had 87.5% of outputs considered valid or partially valid.

**Limitations reported:**
The paper states that the system still needs to be adjusted to work for more types of issues, reducing the need for manual fixes. It also states that human review is still indispensable after bug report generation.

---

## Evidence 12

**Paper:** Yang (2025), *CTQRS-Based Reinforcement Learning Framework for Reliable Bug Report Generation Using Open-Source Large Language Models*, Applied Sciences.
**URL:** https://www.mdpi.com/2076-3417/15/23/12545

**Tool / LLM:** Qwen2.5-7B-Instruct, SFT, PPO reinforcement learning, self-critic refinement

**Dataset:** 3,966 high-quality Bugzilla reports filtered from about 15,000 reports

**Metric:** CTQRS, SBERT, ROUGE-1 Recall/F1, reward convergence

**Result:**
The framework directly optimizes bug report quality using CTQRS as a reward signal. Reported results show CTQRS improved from 0.46 to 0.76, SBERT from 0.68 to 0.85, and ROUGE from 0.52 to 0.63 across training stages.

**Limitations reported:**
The paper states that the model was trained and validated using high-quality reports, so direct capability to enhance low-quality or incomplete reports was not quantitatively evaluated in this version.

---

## Evidence 13

**Paper:** Gonzaga et al. (2025), *Improving Bug Reporting by Fine-Tuning the T5 Model: An Evaluation in a Software Industry*, SAST.
**URL:** https://sol.sbc.org.br/index.php/sast/article/view/36893

**Tool / LLM:** Fine-tuned T5-Base models

**Dataset:** 1,800 real bug reports from a software industry testing team

**Metric:** BLEU, METEOR, Precision, Recall, F1-score, success/failure rate, tester validation

**Result:**
Specialized T5 models improve automatic bug report generation. The best model reports BLEU 0.9845, METEOR 0.9634, Precision 0.9898, Recall 0.9886, F1-score 0.9892, and 70% practical success rate.

**Limitations reported:**
The paper states that the model still has hallucinations/failures and future work should use more robust T5 models and larger datasets with greater processing power.

---

## Evidence 14

**Paper:** Dinç et al. (2025), *Judge the Votes: A System to Classify Bug Reports and Give Suggestions*, AIware.

**Tool / LLM:** RoBERTa, Random Forest, SVM, GPT-based Judge LLM, RAG

**Dataset:** 10,000 Mozilla Firefox bug reports; 8,000 train, 2,000 test

**Metric:** F1-score

**Result:**
RoBERTa achieved F1 = 0.909. Judge LLM achieved F1 = 0.871. RAG-enhanced LLM achieved F1 = 0.815. Zero-shot LLM achieved F1 between 0.531 and 0.737.

**Limitations reported:**
LLM approaches performed worse than the fine-tuned RoBERTa model. The evaluation used only the Firefox dataset.

---

## Evidence 15

**Paper:** Wang et al. (2024), *Feedback-Driven Automated Whole Bug Report Reproduction for Android Apps*, ISSTA 2024.
**DOI:** 10.1145/3650212.3680341

**Tool / LLM:** GPT-4 based framework (ReBL)

**Dataset:** 96 Android bug reports; 73 crash reports and 23 non-crash reports

**Metric:** Bug reproduction success rate; reproduction time

**Result:**
ReBL successfully reproduced 90.63% of evaluated bug reports and achieved an average reproduction time of 74.98 seconds per report. The evidence table reports that ReBL outperformed existing baseline approaches in success rate and execution speed.

**Limitations reported:**
The study focuses on Android applications and relies on GPT-4. Generalization to other software domains was not fully evaluated.

---

## Evidence 16

**Paper:** Feng & Chen (2024), *Prompting Is All You Need: Automated Android Bug Replay with Large Language Models*, ICSE 2024.
**DOI / URL:** 10.48550/arXiv.2306.01987

**Tool / LLM:** AdbGPT using Large Language Models with few-shot prompting and chain-of-thought reasoning

**Dataset:** Android bug reports

**Metric:** Bug replay success rate; execution time

**Result:**
AdbGPT automatically reproduces Android bugs from bug reports through prompt engineering without additional model training. The paper reports successful replay of 81.3% of bug reports with an average execution time of 253.6 seconds.

**Limitations reported:**
The evaluation was conducted in a limited Android bug replay setting and may require adaptation for other platforms or software systems.

---