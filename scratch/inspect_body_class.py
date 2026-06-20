import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1198,788")

driver = webdriver.Chrome(options=options)
try:
    driver.get("http://localhost:8000/dashboard.html")
    # Wait for JS to run
    import time
    time.sleep(1)
    body_class = driver.execute_script("return document.body.className")
    print(f"Body class at 1198px: '{body_class}'")
    
    # Check width of sidebar wrapper
    sidebar_width = driver.execute_script("return document.querySelector('.side-bar-wrapper').offsetWidth")
    print(f"Sidebar wrapper width: {sidebar_width}px")
    
    # Check padding of sidebar wrapper
    sidebar_padding = driver.execute_script("return window.getComputedStyle(document.querySelector('.side-bar-wrapper')).padding")
    print(f"Sidebar wrapper padding: {sidebar_padding}")
    
    # Check background color of sidebar wrapper
    sidebar_bg = driver.execute_script("return window.getComputedStyle(document.querySelector('.side-bar-wrapper')).backgroundColor")
    print(f"Sidebar wrapper background-color: {sidebar_bg}")

finally:
    driver.quit()
