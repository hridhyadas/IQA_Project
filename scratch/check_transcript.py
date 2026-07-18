import json
import os

transcript_path = "C:\\Users\\hp\\.gemini\\antigravity-ide\\brain\\5eb28c00-c745-4348-95dc-e12f64ed648f\\.system_generated\\logs\\transcript.jsonl"

found = 0
if os.path.exists(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if "Exam Management" in line:
                print(f"Line {idx} contains 'Exam Management'")
                found += 1
                # print first 200 chars around it
                pos = line.find("Exam Management")
                print(line[max(0, pos-100):min(len(line), pos+100)])
else:
    print("Transcript path does not exist!")

print("Total occurrences found:", found)
