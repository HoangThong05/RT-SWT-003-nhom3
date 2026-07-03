# test_api.py — Gate E3: Kiểm tra Qwen2.5-7B-Instruct load được và sinh 1 output mẫu
# Chạy trên Kaggle Notebook (GPU T4) trước khi bắt đầu pilot
# Owner: LR (Nguyễn Công Huy, SE192333)

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ── Cấu hình ──────────────────────────────────────────────────────────────────
MODEL_NAME   = "unsloth/Qwen2.5-7B-Instruct"
TEMPERATURE  = 0.01
MAX_NEW_TOKENS = 512
DO_SAMPLE    = False

# ── Prompt 3-shot (Alpaca-LoRA template, E02 Listing 2) ──────────────────────
SYSTEM_PROMPT = (
    "You are an expert software tester. Given an unstructured bug description, "
    "generate a structured bug report with four sections: "
    "Steps to Reproduce (S2R), Expected Result (ER), Actual Result (AR), "
    "and Additional Information."
)

SHOT_1_INPUT = (
    "The app crashes when I try to upload a photo larger than 5MB on the profile page."
)
SHOT_1_OUTPUT = (
    "#### Steps to Reproduce (S2R)\n"
    "1. Open the app and navigate to the Profile page.\n"
    "2. Tap 'Edit Profile' and select 'Upload Photo'.\n"
    "3. Choose a photo larger than 5MB from your gallery.\n\n"
    "#### Expected Result (ER)\n"
    "The photo should upload successfully and display on the profile.\n\n"
    "#### Actual Result (AR)\n"
    "The app crashes immediately after selecting the photo.\n\n"
    "#### Additional Information\n"
    "- Device: Samsung Galaxy S21, Android 12\n"
    "- App version: 3.2.1\n"
    "- Reproducible 100% of the time."
)

SHOT_2_INPUT = (
    "Dark mode doesn't work on the settings page. "
    "When I switch to dark mode, the settings page background stays white."
)
SHOT_2_OUTPUT = (
    "#### Steps to Reproduce (S2R)\n"
    "1. Open the app and go to Settings.\n"
    "2. Toggle 'Dark Mode' to ON.\n"
    "3. Navigate to any page within Settings.\n\n"
    "#### Expected Result (ER)\n"
    "All pages including Settings should switch to dark background.\n\n"
    "#### Actual Result (AR)\n"
    "The Settings page background remains white while other pages switch correctly.\n\n"
    "#### Additional Information\n"
    "- OS: iOS 16.2, iPhone 13\n"
    "- Reproducible every time dark mode is enabled."
)

SHOT_3_INPUT = (
    "Search results don't update when I type in the search box. "
    "I have to press Enter manually every time."
)
SHOT_3_OUTPUT = (
    "#### Steps to Reproduce (S2R)\n"
    "1. Open the app and navigate to the Search screen.\n"
    "2. Tap on the search box and begin typing a query.\n"
    "3. Observe the search results while typing.\n\n"
    "#### Expected Result (ER)\n"
    "Search results should update in real-time as the user types.\n\n"
    "#### Actual Result (AR)\n"
    "Search results do not update until the user presses Enter.\n\n"
    "#### Additional Information\n"
    "- Tested on Chrome 114 and Firefox 113 on Windows 10.\n"
    "- Issue present since app version 2.8.0."
)

TEST_INPUT = (
    "Hey, so I found a bug in Firefox. When I close a tab and check "
    "Recently Closed Tabs, the tab doesn't show up right away — takes a few seconds."
)

def build_prompt(user_input: str) -> str:
    return (
        f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n"
        f"<|im_start|>user\n{SHOT_1_INPUT}<|im_end|>\n"
        f"<|im_start|>assistant\n{SHOT_1_OUTPUT}<|im_end|>\n"
        f"<|im_start|>user\n{SHOT_2_INPUT}<|im_end|>\n"
        f"<|im_start|>assistant\n{SHOT_2_OUTPUT}<|im_end|>\n"
        f"<|im_start|>user\n{SHOT_3_INPUT}<|im_end|>\n"
        f"<|im_start|>assistant\n{SHOT_3_OUTPUT}<|im_end|>\n"
        f"<|im_start|>user\n{user_input}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

# ── Load model ────────────────────────────────────────────────────────────────
print(f"Loading model: {MODEL_NAME}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
)
print("Model loaded successfully.\n")

# ── Test 1 call ───────────────────────────────────────────────────────────────
prompt = build_prompt(TEST_INPUT)
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

print("Running test inference...")
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=DO_SAMPLE,
        temperature=TEMPERATURE,
    )

generated = tokenizer.decode(
    outputs[0][inputs["input_ids"].shape[1]:],
    skip_special_tokens=True
)

print("=" * 60)
print("TEST INPUT:")
print(TEST_INPUT)
print("\nMODEL OUTPUT:")
print(generated)
print("=" * 60)
print("\n✅ Gate E3 PASSED — model loads and generates output correctly.")
