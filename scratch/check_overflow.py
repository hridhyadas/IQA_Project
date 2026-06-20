from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def check_layout_at_resolution(width, height):
    options = Options()
    options.add_argument("--headless")
    options.add_argument(f"--window-size={width + 14},{height + 94}") # adjust window size to hit exact inner viewport
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get("http://localhost:8000/dashboard.html")
        time.sleep(1)
        
        # 1. Closed state
        client_w = driver.execute_script("return document.documentElement.clientWidth")
        scroll_w = driver.execute_script("return document.documentElement.scrollWidth")
        body_class = driver.execute_script("return document.body.className")
        print(f"Viewport: {client_w}x{height} (Body Class: '{body_class}')")
        print(f"  Closed state scrollWidth: {scroll_w}px")
        if scroll_w > client_w:
            print("  [ERROR] Horizontal scrollbar detected in CLOSED state!")
            print_overflow_elements(driver)
            
        # 2. Click toggle button to open
        toggle_btn = driver.find_element("css selector", ".side-bar-close")
        driver.execute_script("arguments[0].click();", toggle_btn)
        time.sleep(1)
        
        # 3. Open state
        client_w = driver.execute_script("return document.documentElement.clientWidth")
        scroll_w = driver.execute_script("return document.documentElement.scrollWidth")
        body_class = driver.execute_script("return document.body.className")
        print(f"  Open state scrollWidth: {scroll_w}px (Body Class: '{body_class}')")
        if scroll_w > client_w:
            print("  [ERROR] Horizontal scrollbar detected in OPEN state!")
            print_overflow_elements(driver)
            
    finally:
        driver.quit()

def print_overflow_elements(driver):
    overflowing_elements = driver.execute_script("""
        var elements = document.querySelectorAll('*');
        var out = [];
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            var rect = el.getBoundingClientRect();
            if (rect.right > window.innerWidth || rect.left < 0) {
                out.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    rect: rect
                });
            }
        }
        return out;
    """)
    print(f"  Overflowing elements:")
    for el in overflowing_elements[:10]:
        print(f"    - {el['tag']}.{el['className'].replace(' ', '.')} (id={el['id']}): rect={el['rect']}")

if __name__ == "__main__":
    print("--- Checking 1198px ---")
    check_layout_at_resolution(1198, 900)
    print("--- Checking 1024px ---")
    check_layout_at_resolution(1024, 768)
    print("--- Checking 768px ---")
    check_layout_at_resolution(768, 1024)
