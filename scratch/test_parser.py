import re

html_path = r"d:\New folder\IQA_Project\dashboard.html"

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Let's count how many academy-icon-circle classes we have
academy_matches = list(re.finditer(r'<div class="academy-icon-circle">', html_content))
print(f"Found {len(academy_matches)} occurrences of academy-icon-circle")

exam_matches = list(re.finditer(r'<div class="exam-icon-circle[^"]*">', html_content))
print(f"Found {len(exam_matches)} occurrences of exam-icon-circle")
