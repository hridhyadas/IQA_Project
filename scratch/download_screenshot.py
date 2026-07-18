import urllib.request
import re
import os

def download_lightshot(url, output_name):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    )
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # Look for the image source. Lightshot uses <img class="no-click screenshot-image" src="..." or similar
        # Let's search for src containing image.prntscr.com or similar
        matches = re.findall(r'src="([^"]+)"', html)
        img_url = None
        for m in matches:
            if 'image.prntscr.com' in m or 'prntscr' in m or 'cloud.lightshot' in m:
                img_url = m
                break
        if not img_url:
            # Fallback regex search for property="og:image"
            og_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
            if og_match:
                img_url = og_match.group(1)
        
        if img_url:
            print(f"Downloading image from {img_url} to {output_name}")
            urllib.request.urlretrieve(img_url, output_name)
        else:
            print(f"Could not find image URL in HTML for {url}")
            # print first 500 chars of HTML
            print(html[:500])
    except Exception as e:
        print(f"Error downloading {url}: {e}")

os.makedirs('scratch/screenshots', exist_ok=True)
download_lightshot('https://prnt.sc/PNpFElCPv5py', 'scratch/screenshots/figma_create_exam.png')
download_lightshot('https://prnt.sc/DPKxaSGPFKL8', 'scratch/screenshots/current_create_exam.png')
