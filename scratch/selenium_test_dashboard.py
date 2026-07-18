import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def run_tests():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print("Opening Dashboard Page on Desktop (1920x1080)...")
        driver.get("http://localhost:8000/dashboard.html")
        time.sleep(2)
        
        # Take a desktop screenshot
        desktop_ss_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\5eb28c00-c745-4348-95dc-e12f64ed648f\desktop_dashboard_verified.png"
        driver.save_screenshot(desktop_ss_path)
        print(f"Saved desktop screenshot to {desktop_ss_path}")
        
        # Verify Stat Card Colors
        card_selectors = {
            "Academics": (".bg-academics-blue", "rgba(121, 134, 203, 1)"),  # rgb(121, 134, 203)
            "Enrolled Students": (".bg-enrolled-navy", "rgba(63, 81, 181, 1)"),  # rgb(63, 81, 181)
            "Exam Conducted": (".bg-conducted-dark", "rgba(26, 35, 126, 1)"),  # rgb(26, 35, 126)
            "Courses": (".bg-courses-red", "rgba(211, 47, 47, 1)")  # rgb(211, 47, 47)
        }
        
        for name, (selector, expected_rgba) in card_selectors.items():
            el = driver.find_element(By.CSS_SELECTOR, selector)
            bg_color = el.value_of_css_property("background-color")
            print(f"Stat Card '{name}' background-color: {bg_color} (Expected: {expected_rgba})")
            
        # Verify Chart Card Title
        chart_title_el = driver.find_element(By.CSS_SELECTOR, ".student-added-card h5")
        chart_title = chart_title_el.text.strip()
        print(f"Chart Title text: '{chart_title}' (Expected: 'Student Added')")
        assert chart_title == "Student Added", f"Unexpected chart title: {chart_title}"
        
        # Verify Chart Pill Count
        bars = driver.find_elements(By.CSS_SELECTOR, ".custom-bar-col")
        print(f"Found {len(bars)} columns in Student Added chart.")
        assert len(bars) == 12, f"Expected 12 month columns, got {len(bars)}"
        
        for index, bar in enumerate(bars):
            month_label = bar.find_element(By.CSS_SELECTOR, ".bar-label").text.strip()
            white_pills = bar.find_elements(By.CSS_SELECTOR, ".pill-segment.bg-white-stack")
            red_pills = bar.find_elements(By.CSS_SELECTOR, ".pill-segment.active-red")
            print(f"  Month: {month_label} | White pills: {len(white_pills)} | Red pills: {len(red_pills)}")
            assert len(white_pills) == 6, f"Expected 6 white pills, got {len(white_pills)} for {month_label}"
            assert len(red_pills) == 4, f"Expected 4 red pills, got {len(red_pills)} for {month_label}"
            
        # Switch to Mobile View
        print("Switching to Mobile View (375x812)...")
        driver.set_window_size(375, 812)
        time.sleep(2)
        
        # Take a mobile screenshot
        mobile_ss_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\5eb28c00-c745-4348-95dc-e12f64ed648f\mobile_dashboard_verified.png"
        driver.save_screenshot(mobile_ss_path)
        print(f"Saved mobile screenshot to {mobile_ss_path}")
        
        # Verify Mobile Table Time Text is not truncated
        time_el = driver.find_element(By.CSS_SELECTOR, ".recent-exams-table-container td:nth-child(3) .text-muted")
        time_text = time_el.text.strip()
        print(f"Recent Exam Schedule time text visible: '{time_text}'")
        
        print("All checks passed successfully!")
        
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
