# ============================================================
# Script cho MS — Tính CTQRS/ROUGE-1/SBERT + Statistical Test
# Bug Report Quality Assessment with LLM
# ============================================================
# CÁCH DÙNG:
# 1. Chạy trên Kaggle/Colab hoặc máy có GPU/CPU đủ mạnh (Stanza cần tải model NLP)
# 2. Upload full_llm_output.csv (262 dòng, từ LR) vào môi trường
# 3. Chạy lần lượt các cell dưới
# ============================================================

# ----- CELL 1: Cài thư viện -----
# !pip install -q rouge-score sentence-transformers scipy textstat stanza pandas

# ----- CELL 2: Tải model Stanza (chỉ cần 1 lần) -----
import stanza
# stanza.download('en')  # bỏ comment khi chạy lần đầu

nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')

# ----- CELL 3: CTQRS Scorer (code gốc từ GindeLab repo, max_possible=16) -----
import pandas as pd
import os
import re
import textstat

def load_word_list(filename, column_name=None):
    """Tải danh sách từ từ file CSV. Nếu không tìm thấy, trả về set rỗng.
    Nếu không chỉ định column_name, tự lấy cột đầu tiên trong file."""
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        col = column_name if column_name else df.columns[0]
        return set(df[col].dropna().astype(str).str.strip().str.lower())
    return set()

# Tên file và tên cột khớp đúng với file thật tải từ GindeLab repo
WORD_LIST_DIR = "/kaggle/input/datasets/huyncse192333/ctqrs-word-list"
USER_DIRECT_VERBS = load_word_list(f"{WORD_LIST_DIR}/final_unique_behaviours.csv", "Filtered_Unique_Behaviours")
INTERFACE_ELEMENT_WORDS = load_word_list(f"{WORD_LIST_DIR}/interactive_elements.csv", "Nouns")
SYSTEM_DEFECT_WORDS = load_word_list(f"{WORD_LIST_DIR}/_negative_words.csv", "Negative Words")

ENVIRONMENT_WORDS = {"android", "ios", "chrome", "firefox", "windows", "macos"}
SCREENSHOT_WORDS = {"screenshot", "attached image", "see attachment"}
SCREENSHOT_GUIDELINE_WORDS = {"please see", "as shown in the image", "attachment"}
if not INTERFACE_ELEMENT_WORDS:
    INTERFACE_ELEMENT_WORDS = {"adapter", "button", "page", "menu", "dialog", "tab", "screen"}
if not SYSTEM_DEFECT_WORDS:
    SYSTEM_DEFECT_WORDS = {"crash", "down", "flashback", "overlap", "too big", "too small", "freeze"}
if not USER_DIRECT_VERBS:
    USER_DIRECT_VERBS = {"login", "register", "logout"}


def check_RM1_size(text, min_tokens=50, max_tokens=300):
    tokens = text.split()
    return (min_tokens <= len(tokens) <= max_tokens, 1) if min_tokens <= len(tokens) <= max_tokens else (False, 0)

def check_RM2_readability(text, min_score=30, max_score=100):
    if not text.strip():
        return False, 0
    score = textstat.flesch_reading_ease(text)
    return (min_score <= score <= max_score, 1 if min_score <= score <= max_score else 0)

def check_RM3_punctuation(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text.strip()) if s.strip()]
    for s in sentences:
        if not re.match(r'.+[.!?]$', s + "."):
            return False, 0
    return True, 1

def check_RM4_avg_sentence_length(doc, min_len=5, max_len=40):
    sents = list(doc.sentences)
    if not sents:
        return False, 0
    lengths = [len(sent.words) for sent in sents]
    avg_len = sum(lengths) / len(lengths)
    return (min_len <= avg_len <= max_len, 1) if min_len <= avg_len <= max_len else (False, 0)

def check_RR1_itemization(text):
    return (True, 1) if re.search(r'^(\d+\)|-|\*)', text, flags=re.MULTILINE) else (False, 0)

def check_RR2_itemization_symbol(text):
    return (True, 1) if re.search(r'^(-|\*)', text, flags=re.MULTILINE) else (False, 0)

def check_RR3_environment(text):
    text_lower = text.lower()
    for word in ENVIRONMENT_WORDS:
        if word in text_lower:
            return True, 2
    return False, 0

def check_RR4_screenshot(text):
    text_lower = text.lower()
    return (True, 1) if any(w in text_lower for w in SCREENSHOT_WORDS) else (False, 0)

def check_RR5_screenshot_guideline(text):
    text_lower = text.lower()
    return (True, 1) if any(w in text_lower for w in SCREENSHOT_GUIDELINE_WORDS) else (False, 0)


def get_phrase_with_modifiers(sentence, word_id):
    word = sentence.words[word_id - 1]
    modifiers = [w.text for w in sentence.words if w.head == word_id]
    return word.text + ' ' + ' '.join(modifiers)

def has_location_preposition(sentence, word_id):
    return any(w.head == word_id and w.upos == 'ADP' and w.text.lower() in ['in', 'on', 'at'] for w in sentence.words)

def has_time_preposition(sentence, word_id):
    return any(w.head == word_id and w.upos == 'ADP' and w.text.lower() in ['during', 'after', 'before'] for w in sentence.words)


def check_RA1_interface_element(text):
    doc = nlp(text)
    text_lower = text.lower()
    if not any(w in text_lower for w in INTERFACE_ELEMENT_WORDS):
        return False, 0

    relation_mapping = {
        'ATT': ['amod', 'nmod', 'nummod', 'det', 'compound', 'case', 'mark'],
        'ADV': ['advmod', 'advcl', 'obl', 'neg'],
        'CMP': ['obj', 'iobj', 'xcomp', 'ccomp', 'acl'],
        'COO': ['conj', 'cc'],
        'LAD': ['acl:relcl', 'acl'],
        'RAD': ['appos', 'parataxis']
    }
    relation_lookup = {ud: rel for rel, uds in relation_mapping.items() for ud in uds}

    max_relation_score = 0
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.lemma.lower() in INTERFACE_ELEMENT_WORDS:
                relations = {k: 0 for k in ['ATT', 'ADV', 'CMP', 'COO', 'LAD', 'RAD']}
                for other_word in sentence.words:
                    if other_word.head == word.id:
                        rel_type = relation_lookup.get(other_word.deprel)
                        if rel_type:
                            relations[rel_type] += 1
                if word.head != 0:
                    rel_type = relation_lookup.get(word.deprel)
                    if rel_type:
                        relations[rel_type] += 1
                total = sum(relations.values())
                score = 2 if total >= 4 else (1 if total >= 2 else 0)
                max_relation_score = max(max_relation_score, score)
    return max_relation_score > 0, max_relation_score


def check_RA2_user_behavior(text):
    doc = nlp(text)
    text_lower = text.lower()
    if any(verb in text_lower for verb in USER_DIRECT_VERBS):
        return True, 2

    for sentence in doc.sentences:
        predicates = [w for w in sentence.words if w.upos == 'VERB']
        for verb in predicates:
            obj_deps = [w for w in sentence.words if w.head == verb.id and w.deprel in ['obj', 'iobj']]
            for obj in obj_deps:
                obj_phrase = get_phrase_with_modifiers(sentence, obj.id)
                if any(e in obj_phrase.lower() for e in INTERFACE_ELEMENT_WORDS):
                    return True, 2

        has_loc = any(w.deprel in ['obl', 'advmod'] and
                      (any(lw in w.text.lower() for lw in ['in','on','at','page','screen','window']) or has_location_preposition(sentence, w.id))
                      for w in sentence.words)
        has_tmp = any(w.deprel in ['obl', 'advmod'] and
                      (any(tw in w.text.lower() for tw in ['during','when','while','after','before']) or has_time_preposition(sentence, w.id))
                      for w in sentence.words)
        if has_loc and has_tmp:
            return True, 2
        elif has_loc or has_tmp:
            return True, 1
    return False, 0


def check_RA3_system_defect(text):
    doc = nlp(text)
    text_lower = text.lower()
    if any(d in text_lower for d in SYSTEM_DEFECT_WORDS):
        return True, 2

    for sentence in doc.sentences:
        for verb in [w for w in sentence.words if w.upos == 'VERB']:
            has_negation = any(w.deprel == 'advmod' and w.text.lower() in ['not', "n't", 'never', 'no']
                              for w in sentence.words if w.head == verb.id)
            if has_negation:
                system_actions = ["load", "display", "show", "appear", "refresh", "update", "work", "function"]
                is_system_action = any(a in verb.lemma.lower() for a in system_actions)
                has_interface_object = any(w.deprel == 'obj' and any(e in w.lemma.lower() for e in INTERFACE_ELEMENT_WORDS)
                                          for w in sentence.words if w.head == verb.id)
                return (True, 2) if (is_system_action or has_interface_object) else (True, 1)
    return False, 0


def check_RA4_defect_description_quality(text):
    has_defect, _ = check_RA3_system_defect(text)
    if not has_defect:
        return False, 0

    doc = nlp(text)
    relation_mapping = {
        'ATT': ['amod', 'nmod', 'nummod', 'det', 'compound', 'case', 'mark'],
        'ADV': ['advmod', 'advcl', 'obl', 'neg'],
        'CMP': ['obj', 'iobj', 'xcomp', 'ccomp', 'acl'],
        'COO': ['conj', 'cc'],
        'LAD': ['acl:relcl', 'acl'],
        'RAD': ['appos', 'parataxis']
    }
    relation_lookup = {ud: rel for rel, uds in relation_mapping.items() for ud in uds}

    max_relation_score = 0
    for sentence in doc.sentences:
        defect_words = [w for w in sentence.words if w.lemma.lower() in SYSTEM_DEFECT_WORDS]
        defect_words += [w for w in sentence.words if w.upos == 'VERB' and
                         any(o.deprel == 'advmod' and o.text.lower() in ['not', "n't", 'never', 'no']
                             for o in sentence.words if o.head == w.id)]
        if not defect_words:
            continue
        for dw in defect_words:
            relations = {k: 0 for k in ['ATT', 'ADV', 'CMP', 'COO', 'LAD', 'RAD']}
            for ow in sentence.words:
                if ow.head == dw.id:
                    rt = relation_lookup.get(ow.deprel)
                    if rt:
                        relations[rt] += 1
            if dw.head != 0:
                rt = relation_lookup.get(dw.deprel)
                if rt:
                    relations[rt] += 1
            total = sum(relations.values())
            score = 2 if total >= 4 else (1 if total >= 2 else 0)
            max_relation_score = max(max_relation_score, score)
    return max_relation_score > 0, max_relation_score


def evaluate_bug_report(text):
    """Tính CTQRS cho 1 bug report. max_possible=16 (đúng theo code gốc GindeLab)."""
    doc = nlp(text)
    results = {
        "RM1_size": check_RM1_size(text),
        "RM2_readability": check_RM2_readability(text),
        "RM3_punctuation": check_RM3_punctuation(text),
        "RM4_sentence_length": check_RM4_avg_sentence_length(doc),
        "RR1_itemization": check_RR1_itemization(text),
        "RR2_itemization_symbol": check_RR2_itemization_symbol(text),
        "RR3_environment": check_RR3_environment(text),
        "RR4_screenshot": check_RR4_screenshot(text),
        "RR5_screenshot_guideline": check_RR5_screenshot_guideline(text),
        "RA1_interface_element": check_RA1_interface_element(text),
        "RA2_user_behavior": check_RA2_user_behavior(text),
        "RA3_system_defect": check_RA3_system_defect(text),
        "RA4_defect_description": check_RA4_defect_description_quality(text)
    }
    total_score = sum(score for _, score in results.values())
    return {"detail_scores": results, "total_score": total_score, "max_possible": 16}


# ----- CELL 4: ROUGE-1 và SBERT -----
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

rouge = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
sbert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def compute_rouge1_f1(generated, reference):
    scores = rouge.score(reference, generated)
    return scores['rouge1'].fmeasure

def compute_sbert_similarity(generated, reference):
    embeddings = sbert_model.encode([generated, reference])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(sim)


# ----- CELL 5: Chạy tính metric trên toàn bộ 262 dòng -----
df = pd.read_csv("/kaggle/input/datasets/huyncse192333/qwen-output-for-metrics/full_llm_output.csv")
print(f"Đang tính metric cho {len(df)} samples...")

ctqrs_scores = []
ctqrs_percent = []
rouge_scores = []
sbert_scores = []

for idx, row in df.iterrows():
    generated = str(row['qwen_output'])
    reference = str(row['ground_truth'])

    # CTQRS
    ctqrs_result = evaluate_bug_report(generated)
    ctqrs_scores.append(ctqrs_result['total_score'])
    ctqrs_percent.append(ctqrs_result['total_score'] / ctqrs_result['max_possible'] * 100)

    # ROUGE-1
    rouge_scores.append(compute_rouge1_f1(generated, reference))

    # SBERT
    sbert_scores.append(compute_sbert_similarity(generated, reference))

    if (idx + 1) % 20 == 0:
        print(f"Đã xử lý {idx+1}/{len(df)}")

df['ctqrs_score'] = ctqrs_scores
df['ctqrs_percent'] = ctqrs_percent
df['rouge1_f1'] = rouge_scores
df['sbert_similarity'] = sbert_scores

df.to_csv("/kaggle/working/full_metrics_output.csv", index=False)
print("Đã lưu full_metrics_output.csv")


# ----- CELL 6: Thống kê mô tả -----
print("\n=== THỐNG KÊ MÔ TẢ (N=262) ===")
print(f"CTQRS %    — median: {np.median(ctqrs_percent):.2f}%, mean: {np.mean(ctqrs_percent):.2f}%, std: {np.std(ctqrs_percent):.2f}")
print(f"ROUGE-1 F1 — median: {np.median(rouge_scores):.4f}, mean: {np.mean(rouge_scores):.4f}, std: {np.std(rouge_scores):.4f}")
print(f"SBERT      — median: {np.median(sbert_scores):.4f}, mean: {np.mean(sbert_scores):.4f}, std: {np.std(sbert_scores):.4f}")


# ----- CELL 7: Wilcoxon signed-rank one-sample test (RQ1, H1.1-H1.3) -----
from scipy.stats import wilcoxon

def wilcoxon_one_sample(data, threshold, metric_name):
    """
    Wilcoxon signed-rank one-sample test: kiểm tra median của `data` có >= threshold không.
    H0: median < threshold | H1: median >= threshold
    Cách làm: tính diff = data - threshold, test xem diff có median > 0 có ý nghĩa không.
    """
    diff = np.array(data) - threshold
    diff_nonzero = diff[diff != 0]  # Wilcoxon yêu cầu loại bỏ giá trị 0
    if len(diff_nonzero) == 0:
        print(f"{metric_name}: Tất cả giá trị bằng threshold, không thể test.")
        return None
    stat, p_value = wilcoxon(diff_nonzero, alternative='greater')
    median_val = np.median(data)
    result = "ĐẠT" if (p_value < 0.05 and median_val >= threshold) else "KHÔNG ĐẠT"
    print(f"{metric_name}: median={median_val:.4f}, threshold={threshold}, p-value={p_value:.6f} → {result}")
    return {"metric": metric_name, "median": median_val, "threshold": threshold, "p_value": p_value, "result": result}

print("\n=== WILCOXON SIGNED-RANK ONE-SAMPLE TEST (RQ1, α=0.05) ===")
h1_1 = wilcoxon_one_sample(ctqrs_percent, 75, "H1.1 CTQRS (threshold=75%)")
h1_2 = wilcoxon_one_sample(sbert_scores, 0.82, "H1.2 SBERT (threshold=0.82)")
h1_3 = wilcoxon_one_sample(rouge_scores, 0.47, "H1.3 ROUGE-1 (threshold=0.47)")

# Bonferroni correction nếu cần diễn giải kết hợp 3 test
alpha_adjusted = 0.05 / 3
print(f"\nBonferroni-adjusted alpha (3 tests): {alpha_adjusted:.4f}")


# ----- CELL 8: Cliff's Delta (effect size) -----
def cliffs_delta(data, threshold):
    """Cliff's delta cho one-sample so với threshold cố định."""
    data = np.array(data)
    greater = np.sum(data > threshold)
    less = np.sum(data < threshold)
    n = len(data)
    delta = (greater - less) / n
    return delta

print("\n=== EFFECT SIZE (Cliff's Delta) ===")
print(f"CTQRS:   δ = {cliffs_delta(ctqrs_percent, 75):.3f}")
print(f"SBERT:   δ = {cliffs_delta(sbert_scores, 0.82):.3f}")
print(f"ROUGE-1: δ = {cliffs_delta(rouge_scores, 0.47):.3f}")
