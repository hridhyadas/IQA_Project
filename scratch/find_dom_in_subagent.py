import json

transcript_path = "C:\\Users\\hp\\.gemini\\antigravity-ide\\brain\\5eb28c00-c745-4348-95dc-e12f64ed648f\\.system_generated\\logs\\transcript_full.jsonl"

with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if "Exam Managment" in line:
            print(f"Line {idx} in full transcript contains 'Exam Managment'")
        if "Exam Management" in line:
            print(f"Line {idx} in full transcript contains 'Exam Management'")
