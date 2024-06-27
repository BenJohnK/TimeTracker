from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://wa.me/+918590063863/")
#    page.wait_for_timeout(5000)
    page.screenshot(path="q.png")
    browser.close()