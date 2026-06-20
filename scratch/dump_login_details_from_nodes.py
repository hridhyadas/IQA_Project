import json
import os
import glob

cache_dir = r"C:\Users\hp\.mcp-figma\cache"
node_files = glob.glob(os.path.join(cache_dir, "file_nodes_KDaIN4FMLEYDgVU7fJyvll_*.json"))

web_login_id = "4:8646"
mobile_login_id = "4:8679"

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

for fpath in node_files:
    print(f"Reading {fpath}...")
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    nodes_dict = data.get("nodes", {})
    print(f"Found nodes keys: {list(nodes_dict.keys())}")
    
    for nid, ndata in nodes_dict.items():
        # Clean ID
        clean_id = nid.replace("-", ":")
        print(f"Node data root id: {ndata.get('document', {}).get('id')} / clean_id: {clean_id}")
        
        doc = ndata.get("document", {})
        if clean_id == web_login_id or doc.get("id") == web_login_id:
            web_lines = dump_node(doc)
            with open("scratch/web_login_details.txt", "w", encoding="utf-8") as out:
                out.write("\n".join(web_lines))
            print(f"SUCCESS: Dumped web login to scratch/web_login_details.txt ({len(web_lines)} lines)")
            
        if clean_id == mobile_login_id or doc.get("id") == mobile_login_id:
            mobile_lines = dump_node(doc)
            with open("scratch/mobile_login_details.txt", "w", encoding="utf-8") as out:
                out.write("\n".join(mobile_lines))
            print(f"SUCCESS: Dumped mobile login to scratch/mobile_login_details.txt ({len(mobile_lines)} lines)")
