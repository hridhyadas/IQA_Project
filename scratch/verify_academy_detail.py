from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1200,800')

print("Starting headless Chrome browser...")
driver = webdriver.Chrome(options=options)

try:
    driver.get("http://localhost:8000/academy-detail.html")
    time.sleep(2)

    # Force remove preloader if present
    driver.execute_script("""
        var p = document.querySelector('.preloader');
        if (p) p.remove();
        var l = document.querySelector('.loader');
        if (l) l.remove();
    """)
    time.sleep(0.5)

    print("\n--- STEP 1: Verify Page Load and Desktop Layout ---")
    title = driver.title
    print(f"Page Title: {title}")
    
    # Save a screenshot of initial desktop state
    driver.save_screenshot("scratch/screenshots/desktop_detail_initial.png")
    print("Saved desktop_detail_initial.png")

    print("\n--- STEP 2: Verify Separate IDs for Filters ---")
    date_empty = driver.find_element(By.ID, "dateFilterBtnEmpty")
    date_populated = driver.find_element(By.ID, "dateFilterBtnPopulated")
    print(f"Date empty filter button found: {date_empty is not None}")
    print(f"Date populated filter button found: {date_populated is not None}")

    status_empty = driver.find_element(By.ID, "statusDropdownBtnEmpty")
    status_populated = driver.find_element(By.ID, "statusDropdownBtnPopulated")
    print(f"Status empty filter button found: {status_empty is not None}")
    print(f"Status populated filter button found: {status_populated is not None}")

    print("\n--- STEP 3: Interact with Dropdowns ---")
    
    # Click statusDropdownBtnPopulated
    print("Clicking Populated status dropdown...")
    driver.execute_script("arguments[0].click();", status_populated)
    time.sleep(0.5)
    
    # Find options in menu
    options_populated = driver.find_elements(By.CLASS_NAME, "status-option-populated")
    print(f"Found {len(options_populated)} options in Populated status dropdown menu.")
    
    # Select first option ("Action")
    print("Selecting 'Action' option...")
    driver.execute_script("arguments[0].click();", options_populated[0])
    time.sleep(0.5)
    
    updated_populated_text = driver.find_element(By.ID, "statusDropdownTextPopulated").text
    print(f"Populated status filter label text updated to: {updated_populated_text}")
    
    # Save screenshot of updated dropdown
    driver.save_screenshot("scratch/screenshots/desktop_populated_selected.png")
    print("Saved desktop_populated_selected.png")

    # Click statusDropdownBtnEmpty
    print("Clicking Empty status dropdown...")
    driver.execute_script("arguments[0].click();", status_empty)
    time.sleep(0.5)
    
    options_empty = driver.find_elements(By.CLASS_NAME, "status-option-empty")
    print(f"Found {len(options_empty)} options in Empty status dropdown menu.")
    
    # Select second option ("Another action")
    print("Selecting 'Another action' option...")
    driver.execute_script("arguments[0].click();", options_empty[1])
    time.sleep(0.5)
    
    updated_empty_text = driver.find_element(By.ID, "statusDropdownTextEmpty").text
    print(f"Empty status filter label text updated to: {updated_empty_text}")

    print("\n--- STEP 4: Verify Mobile Accordion Layout ---")
    driver.set_window_size(375, 667)
    time.sleep(1)
    
    # Check if elements are hidden/visible appropriately on mobile
    student_table = driver.find_element(By.CSS_SELECTOR, ".recent-exams-table-container table")
    print("Student table class list:", student_table.get_attribute("class"))
    
    # Find expanded/collapsible triggers
    expand_triggers = driver.find_elements(By.CLASS_NAME, "expand-btn")
    print(f"Found {len(expand_triggers)} responsive expand buttons in the tables.")
    
    driver.save_screenshot("scratch/screenshots/mobile_detail_view.png")
    print("Saved mobile_detail_view.png")

finally:
    driver.quit()
    print("Browser closed.")
