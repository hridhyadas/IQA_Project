import os
import sys
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch browser headlessly
        browser = await p.chromium.launch(headless=True)
        # Create context with mobile viewport
        context = await browser.new_context(
            viewport={"width": 375, "height": 800},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )
        page = await context.new_page()
        
        # Navigate to the page
        await page.goto("http://localhost:5500/IQA_Project/academy-list.html")
        # Give it a moment to load and run scripts
        await page.wait_for_timeout(2000)
        
        # Extract the table outerHTML
        table_html = await page.eval_on_selector("#academyTable", "el => el.outerHTML")
        
        print("--- TABLE DOM START ---")
        print(table_html)
        print("--- TABLE DOM END ---")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
