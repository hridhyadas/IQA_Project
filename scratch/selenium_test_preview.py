from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

print("Starting headless Chrome browser...")
driver = webdriver.Chrome(options=options)
try:
    driver.get("http://localhost:8000/create-exam-preview.html")
    time.sleep(2)
    
    # Force remove preloader if present
    driver.execute_script("""
        var p = document.querySelector('.preloader');
        if (p) p.remove();
        var l = document.querySelector('.loader');
        if (l) l.remove();
    """)
    time.sleep(0.5)
    
    print("\n--- STEP 1: Verify Initial State ---")
    breadcrumbs = driver.find_element(By.CLASS_NAME, "ed-breadcrumb").text
    print("Breadcrumbs text:\n", breadcrumbs)
    
    steps_card = driver.find_element(By.CLASS_NAME, "steps-card").text
    print("Steps card buttons present:", "Cancel" in steps_card or "Back" in steps_card)
    
    print("\n--- STEP 2: Verify Question Rows Structure ---")
    q_rows = driver.find_elements(By.CLASS_NAME, "qp-question-row")
    print(f"Total question rows: {len(q_rows)}")
    for idx, row in enumerate(q_rows):
        card = row.find_elements(By.CLASS_NAME, "qp-item-card")
        delete = row.find_elements(By.CLASS_NAME, "qp-item-delete")
        print(f"  Row {idx + 1}:")
        print(f"    - Card present: {len(card) > 0}")
        if len(card) > 0:
            print(f"      - Question text: {card[0].find_element(By.CLASS_NAME, 'qp-item-question').text[:50]}...")
        print(f"    - Delete outside card (adjacent child): {len(delete) > 0}")
        
    print("\n--- STEP 3: Test Delete Question Row 1 ---")
    first_row = q_rows[0]
    delete_icon = first_row.find_element(By.CLASS_NAME, "qp-item-delete")
    print("Clicking delete icon...")
    driver.execute_script("arguments[0].click();", delete_icon)
    time.sleep(0.5)
    
    # Handle the javascript confirmation dialog
    try:
        alert = driver.switch_to.alert
        print("Alert text:", alert.text)
        alert.accept()
        print("Alert accepted.")
        time.sleep(1)
    except Exception as e:
        print("No browser alert shown:", e)
        
    q_rows_after = driver.find_elements(By.CLASS_NAME, "qp-question-row")
    print(f"Total question rows after deletion: {len(q_rows_after)}")
    
    print("\n--- STEP 4: Verify Page Level Actions Footer ---")
    footer = driver.find_element(By.CLASS_NAME, "page-footer-actions")
    print("Footer present:", footer is not None)
    
    cancel_btn = footer.find_element(By.CLASS_NAME, "btn-cancel-text")
    print("Cancel text link text:", cancel_btn.text)
    
    back_btn = footer.find_element(By.CLASS_NAME, "btn-outline-back")
    print("Back button text:", back_btn.text)
    
    publish_btn = footer.find_element(By.CLASS_NAME, "btn-publish")
    print("Publish Exam button text:", publish_btn.text)
    
    print("\n--- STEP 5: Test Publish Exam Redirection ---")
    driver.execute_script("arguments[0].click();", publish_btn)
    time.sleep(0.5)
    
    try:
        alert = driver.switch_to.alert
        print("Publish Alert text:", alert.text)
        alert.accept()
        print("Publish Alert accepted.")
        time.sleep(1)
    except Exception as e:
        print("No publish alert shown:", e)
        
    print("URL after publishing:", driver.current_url)
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
