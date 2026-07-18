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
    driver.get("http://localhost:8000/create-exam.html")
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
    
    print("\n--- STEP 2: Transition to Edit State ---")
    add_question_btn = driver.find_element(By.ID, "btn-add-question")
    # Click via JS to prevent preloader interception issues
    driver.execute_script("arguments[0].click();", add_question_btn)
    time.sleep(1)
    
    form_visible = driver.find_element(By.ID, "qm-form-state").is_displayed()
    print("Question Form is visible:", form_visible)
    
    question_title = driver.find_element(By.CSS_SELECTOR, ".qm-form-header h4").text
    print("Question Title text:", question_title)
    
    score_input = driver.find_element(By.CLASS_NAME, "qm-score-input")
    score_val = score_input.get_attribute("value")
    print("Question Score input value:", score_val)
    
    print("\n--- STEP 3: Verify Options & Add Dynamic Option ---")
    options_list = driver.find_elements(By.CSS_SELECTOR, "#options-list-container .qm-option-row")
    print(f"Initial options count: {len(options_list)}")
    for o in options_list:
        print(f"  - Option data-index: {o.get_attribute('data-index')}, value: {o.find_element(By.CLASS_NAME, 'qm-option-input').get_attribute('value')}")
        
    add_option_btn = driver.find_element(By.ID, "btn-add-option-trigger")
    print("Clicking Add Option...")
    driver.execute_script("arguments[0].click();", add_option_btn)
    time.sleep(0.5)
    
    options_list = driver.find_elements(By.CSS_SELECTOR, "#options-list-container .qm-option-row")
    print(f"New options count: {len(options_list)}")
    for o in options_list:
        print(f"  - Option data-index: {o.get_attribute('data-index')}, value: {o.find_element(By.CLASS_NAME, 'qm-option-input').get_attribute('value')}")
        
    print("\n--- STEP 4: Delete Option 2 ---")
    # Delete row with index 2
    row2 = driver.find_element(By.XPATH, "//div[@id='options-list-container']/div[@data-index='2']")
    delete_btn = row2.find_element(By.CLASS_NAME, "qm-option-delete")
    print("Clicking delete on Option 2...")
    driver.execute_script("arguments[0].click();", delete_btn)
    time.sleep(0.5)
    
    options_list = driver.find_elements(By.CSS_SELECTOR, "#options-list-container .qm-option-row")
    print(f"Options count after delete: {len(options_list)}")
    for o in options_list:
        print(f"  - Option data-index: {o.get_attribute('data-index')}, value: {o.find_element(By.CLASS_NAME, 'qm-option-input').get_attribute('value')}")
        
    print("\n--- STEP 5: Pagination - Add Question ---")
    desktop_grid = driver.find_element(By.ID, "desktop-pagination-grid")
    q_btns = desktop_grid.find_elements(By.CLASS_NAME, "qm-page-btn")
    print(f"Initial question buttons count: {len(q_btns)}")
    
    add_q_btn = driver.find_element(By.ID, "btn-add-question-nav")
    print("Clicking Add Question in pagination grid...")
    driver.execute_script("arguments[0].click();", add_q_btn)
    time.sleep(0.5)
    
    q_btns = desktop_grid.find_elements(By.CLASS_NAME, "qm-page-btn")
    print(f"New question buttons count: {len(q_btns)}")
    for btn in q_btns:
        print(f"  - Button text: {btn.text}, active: {'active' in btn.get_attribute('class')}")
        
    new_question_title = driver.find_element(By.CSS_SELECTOR, ".qm-form-header h4").text
    print("Question Title text after adding:", new_question_title)
    
    print("\n--- STEP 6: Verify Page Actions Footer ---")
    footer = driver.find_element(By.CLASS_NAME, "page-footer-actions")
    print("Footer is present:", footer is not None)
    btn_save_next = driver.find_element(By.ID, "btn-page-save-next")
    print("Save & Next button text:", btn_save_next.text)
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
