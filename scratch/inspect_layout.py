import http.server
import socketserver
import subprocess
import time
import json
import os

PORT = 8005
received_data = None

class DataReceiver(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        global received_data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        received_data = json.loads(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-type')
        self.end_headers()

def run_inspector():
    global received_data
    # 1. Inject temporary script into dashboard.html
    dashboard_path = "dashboard.html"
    with open(dashboard_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    script_to_inject = """
    <script>
    window.addEventListener('load', function() {
        setTimeout(function() {
            // Find all elements that overflow the viewport width
            var overflowing_elements = [];
            var all = document.querySelectorAll('*');
            for (var i = 0; i < all.length; i++) {
                var el = all[i];
                var rect = el.getBoundingClientRect();
                if (rect.right > window.innerWidth) {
                    // Get selector or class list
                    var name = el.tagName.toLowerCase();
                    if (el.id) name += '#' + el.id;
                    if (el.className) name += '.' + el.className.split(' ').join('.');
                    overflowing_elements.push({
                        element: name,
                        right: rect.right,
                        width: rect.width,
                        left: rect.left,
                        window_width: window.innerWidth
                    });
                }
            }
            
            var data = {
                body_classes: document.body.className,
                window_width: window.innerWidth,
                window_height: window.innerHeight,
                profile_widget: document.querySelector('.header-profile-widget') ? document.querySelector('.header-profile-widget').getBoundingClientRect() : null,
                header_container_rect: document.querySelector('.header-container') ? document.querySelector('.header-container').getBoundingClientRect() : null,
                content_wrapper_rect: document.querySelector('.content-wrapper') ? document.querySelector('.content-wrapper').getBoundingClientRect() : null
            };
            
            fetch('http://localhost:8005', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).catch(err => console.log(err));
        }, 1000);
    });
    </script>
    """
    
    # Insert before </body>
    temp_html = html.replace("</body>", script_to_inject + "\n</body>")
    temp_dashboard_path = "dashboard_temp.html"
    with open(temp_dashboard_path, "w", encoding="utf-8") as f:
        f.write(temp_html)
        
    # 2. Start local receiver server
    server = socketserver.TCPServer(("", PORT), DataReceiver)
    server.timeout = 10
    
    # 3. Launch Chrome headlessly
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        
    # Start chrome
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--window-size=1198,800",
        "http://localhost:8000/dashboard_temp.html"
    ]
    
    print("Launching Chrome...")
    subprocess.Popen(cmd)
    
    # Wait for server request - loop until we receive the post data
    while received_data is None:
        server.handle_request()
    server.server_close()
    
    # Clean up temp file
    if os.path.exists(temp_dashboard_path):
        os.remove(temp_dashboard_path)
        
    print("\nLAYOUT INSPECTION RESULTS:")
    print(json.dumps(received_data, indent=2))

if __name__ == "__main__":
    run_inspector()
