import urllib.request

try:
    url = "http://localhost:8000/create-exam.html"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    print("Length of fetched HTML:", len(html))
    
    # Check if "Exam Management" is in the HTML
    if "Exam Management" in html:
        print("Success: 'Exam Management' is in served HTML!")
    else:
        print("Error: 'Exam Management' NOT in served HTML!")
        
    if "btn-add-option-trigger" in html:
        print("Success: 'btn-add-option-trigger' is in served HTML!")
    else:
        print("Error: 'btn-add-option-trigger' NOT in served HTML!")
        
    if "page-footer-actions" in html:
        print("Success: 'page-footer-actions' is in served HTML!")
    else:
        print("Error: 'page-footer-actions' NOT in served HTML!")
except Exception as e:
    print(f"Error fetching from server: {e}")
