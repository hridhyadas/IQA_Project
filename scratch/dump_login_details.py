import json

cache_path = r"C:\Users\hp\.mcp-figma\cache\file_KDaIN4FMLEYDgVU7fJyvll_1781796055878.json"
with open(cache_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find the children of Page 1
page1 = None
for child in data["document"]["children"]:
    if child["type"] == "CANVAS" and child["name"] == "Page 1":
        page1 = child
        break

if not page1:
    print("Page 1 not found")
    exit()

def get_fill_colors(node):
    fills = node.get("fills", [])
    colors = []
    for fill in fills:
        if fill.get("type") == "SOLID" and "color" in fill:
            c = fill["color"]
            r = int(c.get("r", 0) * 255)
            g = int(c.get("g", 0) * 255)
            b = int(c.get("b", 0) * 255)
            a = fill.get("opacity", 1)
            colors.append(f"#{r:02X}{g:02X}{b:02X} (opacity: {a:.2f})")
    return ", ".join(colors) if colors else ""

def dump_node(node, depth=0):
    lines = []
    node_type = node.get("type", "UNKNOWN")
    node_name = node.get("name", "")
    node_id = node.get("id", "")
    
    # Get bounds
    bounds = node.get("absoluteBoundingBox", {})
    bounds_str = f"({int(bounds.get('width', 0))}x{int(bounds.get('height', 0))}) at ({int(bounds.get('x', 0))},{int(bounds.get('y', 0))})" if bounds else ""
    
    fills_str = ""
    fills = get_fill_colors(node)
    if fills:
        fills_str = f" | fills={fills}"
        
    text_str = ""
    if node_type == "TEXT":
        text_str = f" | text='{node.get('characters', '').strip()}'"
        style = node.get("style", {})
        font_family = style.get("fontFamily", "")
        font_weight = style.get("fontWeight", "")
        font_size = style.get("fontSize", "")
        text_str += f" | font={font_family} {font_weight} {font_size}px"
        
    indent = "  " * depth
    lines.append(f"{indent}- [{node_type}] '{node_name}' (ID: {node_id}) {bounds_str}{fills_str}{text_str}")
    
    for child in node.get("children", []):
        lines.extend(dump_node(child, depth + 1))
        
    return lines

web_login_id = "4:8646"
mobile_login_id = "4:8679"

web_node = None
mobile_node = None

for child in page1["children"]:
    if child["id"] == web_login_id:
        web_node = child
    elif child["id"] == mobile_login_id:
        mobile_node = child

if web_node:
    web_lines = dump_node(web_node)
    with open("scratch/web_login_details.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(web_lines))
    print(f"Dumped web login details to scratch/web_login_details.txt ({len(web_lines)} nodes)")
else:
    print("Web login node not found")

if mobile_node:
    mobile_lines = dump_node(mobile_node)
    with open("scratch/mobile_login_details.txt", "w", encoding="utf-8") as out:
        out.write("\n".join(mobile_lines))
    print(f"Dumped mobile login details to scratch/mobile_login_details.txt ({len(mobile_lines)} nodes)")
else:
    print("Mobile login node not found")
