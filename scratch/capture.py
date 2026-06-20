import os
import subprocess
import time

def get_chrome_path():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\LocalApp\Google\Chrome\Application\chrome.exe" # alternative
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return "chrome.exe" # fallback to PATH

def capture_screenshot(url, output_path, width=1198, height=2000):
    # Determine the local file path from URL
    filename = url.split("/")[-1]
    temp_filename = "temp_" + filename
    
    # Read original file and inject inline style to hide preloader
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Hide preloader
    html = html.replace('class="preloader"', 'class="preloader" style="display:none !important;"')
    
    # Write temporary file
    with open(temp_filename, "w", encoding="utf-8") as f:
        f.write(html)
        
    chrome = get_chrome_path()
    local_url = f"http://localhost:8000/{temp_filename}"
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        f"--screenshot={output_path}",
        local_url
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)
    
    # Clean up temp file
    if os.path.exists(temp_filename):
        os.remove(temp_filename)

if __name__ == "__main__":
    brain_dir = r"C:\Users\hp\.gemini\antigravity-ide\brain\998db5f1-e073-4404-a50f-511a6024bcd9"
    os.makedirs(brain_dir, exist_ok=True)
    
    # 1. Capture Dashboard at 1198px
    capture_screenshot(
        "http://localhost:8000/dashboard.html",
        os.path.join(brain_dir, "verify_dashboard_1198_full.png"),
        width=1198,
        height=3500
    )
    
    # 2. Capture Login at 1198px
    capture_screenshot(
        "http://localhost:8000/login.html",
        os.path.join(brain_dir, "verify_login_1198_full.png"),
        width=1198,
        height=1000
    )
    
    # 3. Capture Dashboard at 1024px
    capture_screenshot(
        "http://localhost:8000/dashboard.html",
        os.path.join(brain_dir, "verify_dashboard_1024_full.png"),
        width=1024,
        height=3500
    )
    
    print("Done capturing!")
