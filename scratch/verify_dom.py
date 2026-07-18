import urllib.request
import re

url = "http://localhost:8000/create-exam.html"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})
html = urllib.request.urlopen(req).read().decode('utf-8')

print("=== SERVER SIDE HTML VERIFICATION ===")
print("Sidebar checks:")
if "Exam Management" in html:
    print("  [OK] 'Exam Management' exists.")
else:
    print("  [FAIL] 'Exam Management' missing.")

if "Create Exam" in html:
    print("  [OK] 'Create Exam' exists.")
else:
    print("  [FAIL] 'Create Exam' missing.")

print("Stepper card checks:")
if "Cancel" in html and "btn-steps-cancel" in html:
    # Check if the btn-steps-cancel is inside the steps-card
    # Let's search steps-card content
    steps_card_match = re.search(r'<div class="steps-card">.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
    if steps_card_match:
        content = steps_card_match.group(0)
        if "btn-steps-cancel" in content:
            print("  [FAIL] Action buttons still present inside steps-card!")
        else:
            print("  [OK] Action buttons removed from steps-card.")
    else:
        print("  [WARNING] Could not find steps-card in HTML using regex.")
else:
    print("  [OK] Action buttons not present.")

print("Question card header checks:")
if "qm-score-input" in html:
    print("  [OK] 'qm-score-input' exists (Score is input).")
else:
    print("  [FAIL] 'qm-score-input' missing.")

print("Options checks:")
if "btn-add-option-trigger" in html:
    print("  [OK] '+ Add Option' button exists.")
else:
    print("  [FAIL] '+ Add Option' button missing.")

if "options-count-select" in html:
    print("  [FAIL] 'options-count-select' dropdown still exists!")
else:
    print("  [OK] 'options-count-select' dropdown removed.")

print("Delete question card checks:")
if "btn-delete-question-card" in html:
    print("  [OK] 'Delete Question' button exists in card.")
else:
    print("  [FAIL] 'Delete Question' button missing.")

print("Pagination card checks:")
if "btn-add-question-nav" in html:
    print("  [OK] '+ Add Question' button exists.")
else:
    print("  [FAIL] '+ Add Question' button missing.")

print("Page actions footer checks:")
if "page-footer-actions" in html:
    print("  [OK] 'page-footer-actions' container exists.")
else:
    print("  [FAIL] 'page-footer-actions' missing.")
