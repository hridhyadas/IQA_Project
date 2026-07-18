import os

css_files = [os.path.join('css', f) for f in os.listdir('css') if f.endswith('.css')]

print("--- Searching for qm-option in CSS ---")
for f in css_files:
    with open(f, encoding='utf-8') as file:
        content = file.read()
    
    for idx, line in enumerate(content.splitlines()):
        if 'qm-option' in line:
            print(f"{f}:{idx+1}: {line.strip()}")
