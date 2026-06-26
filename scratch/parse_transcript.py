import json
import re

def extract_table_dom():
    path = r"C:\Users\hridh\.gemini\antigravity-ide\brain\006fbf6b-ae12-4b77-8c59-9c46ad4cf691\.system_generated\logs\transcript_full.jsonl"
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if "academyTable" in line and "responsive-applied" in line:
                # Find all occurrences of the HTML string inside this JSON line
                matches = re.findall(r'"html":"([^"]+)"', line)
                if matches:
                    for html_str in matches:
                        # Unescape the HTML string
                        html = html_str.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\/', '/')
                        if 'id="academyTable"' in html:
                            print(f"Found table HTML at line {i}:")
                            print(html)
                            print("="*80)
                            return
                # Also check tool response format
                try:
                    data = json.loads(line)
                    if data.get("type") == "TOOL_RESPONSE" and "content" in data:
                        content = data["content"]
                        if isinstance(content, str) and 'id="academyTable"' in content:
                            print(f"Found table HTML in TOOL_RESPONSE string at line {i}:")
                            print(content)
                            print("="*80)
                            return
                        elif isinstance(content, dict) and "html" in content and 'id="academyTable"' in content["html"]:
                            print(f"Found table HTML in TOOL_RESPONSE dict at line {i}:")
                            print(content["html"])
                            print("="*80)
                            return
                except:
                    pass

if __name__ == "__main__":
    extract_table_dom()
