# ============================================================
# CTQRS SCORER — BẢN ĐÃ SỬA (v2)
# Xử lý 2 vấn đề phát hiện qua debug:
#   1. RA1/RA2/RA3 pass 100% do word-list chứa từ ngắn <3 ký tự
#      gây match giả (substring match không có word-boundary)
#   2. RM3_punctuation luôn fail do regex split nhầm số thập phân
#      (122.0a1 -> "122", "0a1") và markdown header dính vào câu
# ============================================================
# Dùng để THAY THẾ Cell 3 trong compute_metrics_MS.py
# ============================================================

import pandas as pd
import os
import re
import textstat

def load_word_list(filename, column_name=None, min_length=3):
    """Tải danh sách từ từ file CSV.
    FIX: loại bỏ các 'từ' ngắn hơn min_length ký tự (vd: 'i', 'c', 'ms', 'ss')
    vì các từ ngắn này gây match giả tràn lan khi check substring."""
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        col = column_name if column_name else df.columns[0]
        raw_words = set(df[col].dropna().astype(str).str.strip().str.lower())
        # FIX: chỉ giữ từ có độ dài >= min_length VÀ không chứa khoảng trắng
        # (loại bỏ câu dài bị lẫn vào, như "i couldn't find any..." đã phát hiện)
        filtered_words = {w for w in raw_words if len(w) >= min_length and ' ' not in w and len(w) < 30}
        return filtered_words
    return set()

WORD_LIST_DIR = "/kaggle/input/datasets/huyncse192333/ctqrs-word-list"
USER_DIRECT_VERBS = load_word_list(f"{WORD_LIST_DIR}/final_unique_behaviours.csv", "Filtered_Unique_Behaviours")
INTERFACE_ELEMENT_WORDS = load_word_list(f"{WORD_LIST_DIR}/interactive_elements.csv", "Nouns")
SYSTEM_DEFECT_WORDS = load_word_list(f"{WORD_LIST_DIR}/_negative_words.csv", "Negative Words")

print(f"Sau khi lọc: USER_DIRECT_VERBS={len(USER_DIRECT_VERBS)}, INTERFACE_ELEMENT_WORDS={len(INTERFACE_ELEMENT_WORDS)}, SYSTEM_DEFECT_WORDS={len(SYSTEM_DEFECT_WORDS)}")

ENVIRONMENT_WORDS = {"android", "ios", "chrome", "firefox", "windows", "macos"}
SCREENSHOT_WORDS = {"screenshot", "attached image", "see attachment"}
SCREENSHOT_GUIDELINE_WORDS = {"please see", "as shown in the image", "attachment"}
if not INTERFACE_ELEMENT_WORDS:
    INTERFACE_ELEMENT_WORDS = {"adapter", "button", "page", "menu", "dialog", "tab", "screen"}
if not SYSTEM_DEFECT_WORDS:
    SYSTEM_DEFECT_WORDS = {"crash", "down", "flashback", "overlap", "too big", "too small", "freeze"}
if not USER_DIRECT_VERBS:
    USER_DIRECT_VERBS = {"login", "register", "logout"}


def word_in_text(word, text_lower):
    """FIX: dùng word-boundary regex thay vì substring match thường,
    tránh 'ui' match vào giữa từ khác như 'building', 'guide'..."""
    pattern = r'\b' + re.escape(word) + r'\b'
    return re.search(pattern, text_lower) is not None


def check_RM1_size(text, min_tokens=50, max_tokens=300):
    tokens = text.split()
    return (min_tokens <= len(tokens) <= max_tokens, 1) if min_tokens <= len(tokens) <= max_tokens else (False, 0)

def check_RM2_readability(text, min_score=30, max_score=100):
    if not text.strip():
        return False, 0
    score = textstat.flesch_reading_ease(text)
    return (min_score <= score <= max_score, 1 if min_score <= score <= max_score else 0)

def check_RM3_punctuation(text):
    """FIX v2: bỏ qua markdown header, số thứ tự đầu dòng (1. 2. 3.), URL,
    và số thập phân trước khi split câu — các thành phần này không phải
    'câu' theo nghĩa ngữ pháp nên không nên tính vào kiểm tra dấu câu."""
    cleaned = re.sub(r'^#+\s*.*$', '', text, flags=re.MULTILINE)
    # Bỏ số thứ tự đầu dòng dạng "1. ", "2. " (Markdown ordered list)
    cleaned = re.sub(r'^\s*\d+\.\s+', '', cleaned, flags=re.MULTILINE)
    # Bỏ URL (chứa nhiều dấu . không phải kết thúc câu)
    cleaned = re.sub(r'https?://\S+', '', cleaned)
    # Bảo vệ số thập phân/version number (vd 122.0a1) khỏi bị split nhầm
    cleaned = re.sub(r'(\d)\.(\d)', r'\1<DOT>\2', cleaned)
    sentences = [s.strip() for s in re.split(r'[.!?]', cleaned.strip()) if s.strip()]
    if not sentences:
        return False, 0
    valid_count = 0
    for s in sentences:
        s_restored = s.replace("<DOT>", ".")
        if len(s_restored.split()) >= 2:
            valid_count += 1
    return (valid_count / len(sentences) >= 0.7, 1) if valid_count / len(sentences) >= 0.7 else (False, 0)

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
        if word_in_text(word, text_lower):
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
    if not any(word_in_text(w, text_lower) for w in INTERFACE_ELEMENT_WORDS):
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
            if word.lemma.lower() in INTERFACE_ELEMENT_WORDS and len(word.lemma) >= 3:
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
    if any(word_in_text(verb, text_lower) for verb in USER_DIRECT_VERBS):
        return True, 2

    for sentence in doc.sentences:
        predicates = [w for w in sentence.words if w.upos == 'VERB']
        for verb in predicates:
            obj_deps = [w for w in sentence.words if w.head == verb.id and w.deprel in ['obj', 'iobj']]
            for obj in obj_deps:
                obj_phrase = get_phrase_with_modifiers(sentence, obj.id)
                if any(word_in_text(e, obj_phrase.lower()) for e in INTERFACE_ELEMENT_WORDS):
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
    if any(word_in_text(d, text_lower) for d in SYSTEM_DEFECT_WORDS):
        return True, 2

    for sentence in doc.sentences:
        for verb in [w for w in sentence.words if w.upos == 'VERB']:
            has_negation = any(w.deprel == 'advmod' and w.text.lower() in ['not', "n't", 'never', 'no']
                              for w in sentence.words if w.head == verb.id)
            if has_negation:
                system_actions = ["load", "display", "show", "appear", "refresh", "update", "work", "function"]
                is_system_action = any(a in verb.lemma.lower() for a in system_actions)
                has_interface_object = any(w.deprel == 'obj' and any(word_in_text(e, w.lemma.lower()) for e in INTERFACE_ELEMENT_WORDS)
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
    return {"detail_scores": results, "total_score": total_score, "max_possible": 18}
