import re

html_path = r"d:\New folder\IQA_Project\dashboard.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace top academies
academy_pattern = re.compile(r'(<div class="academy-icon-circle">)\s*<svg.*?</svg>\s*(</div>)', re.DOTALL)

# Let's count how many we can find
matches = list(academy_pattern.finditer(content))
print(f"Academy SVG pattern matches: {len(matches)}")

# Let's replace them one by one, keeping track of index
def academy_replace(match):
    global academy_count
    academy_count += 1
    prefix = match.group(1)
    suffix = match.group(2)
    new_tag = f'\n                      <img src="img/ta{academy_count}.svg" alt="Academy Logo">\n                    '
    return prefix + new_tag + suffix

academy_count = 0
content_new, n = academy_pattern.subn(academy_replace, content)
print(f"Replaced {n} academy SVGs with img tags")

# Replace exams
exam_pattern = re.compile(r'(<div class="exam-icon-circle ms-3">)\s*<svg.*?</svg>\s*(</div>)', re.DOTALL)
matches_exam = list(exam_pattern.finditer(content_new))
print(f"Exam SVG pattern matches: {len(matches_exam)}")

exam_count = 0
def exam_replace(match):
    global exam_count
    exam_count += 1
    prefix = match.group(1)
    suffix = match.group(2)
    alt_texts = ["Calendar Icon", "Broadcast Icon", "Clipboard Icon", "Repeat Icon"]
    alt_text = alt_texts[exam_count - 1] if exam_count <= len(alt_texts) else "Exam Icon"
    new_tag = f'\n                      <img src="img/e{exam_count}.svg" alt="{alt_text}">\n                    '
    return prefix + new_tag + suffix

content_new, n_exam = exam_pattern.subn(exam_replace, content_new)
print(f"Replaced {n_exam} exam SVGs with img tags")

# Let's write the modified content back
with open(html_path, "w", encoding="utf-8") as f:
    f.write(content_new)

print("Done!")
