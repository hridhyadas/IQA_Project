import json

transcript_path = "C:\\Users\\hp\\.gemini\\antigravity-ide\\brain\\5eb28c00-c745-4348-95dc-e12f64ed648f\\.system_generated\\logs\\transcript_full.jsonl"

lines_to_check = [230, 231, 235]
with open(transcript_path, 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if idx in lines_to_check:
            data = json.loads(line)
            print(f"=== Line {idx} ===")
            print("Source:", data.get('source'))
            print("Type:", data.get('type'))
            print("Content snippet:", str(data.get('content'))[:500])
            if 'tool_calls' in data:
                print("Tool calls:", data['tool_calls'])
            print()
