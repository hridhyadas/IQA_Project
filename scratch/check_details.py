import os

css_files = [os.path.join('css', f) for f in os.listdir('css') if f.endswith('.css')]

print("--- Searching for SI in CSS ---")
for f in css_files:
    with open(f, encoding='utf-8') as file:
        content = file.read()
    
    for idx, line in enumerate(content.splitlines()):
        if 'content:' in line and 'SI' in line:
            print(f"{f}:{idx+1}: {line.strip()}")
