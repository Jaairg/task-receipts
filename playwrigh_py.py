from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright

# Find file in path
path = Path("templates/index.html").resolve()
# convert file path to url
url = path.as_uri()


def run(playwright: Playwright):
    # set the browser to use
    chromium = playwright.chromium
    # returns the browser instance
    browser = chromium.launch(headless=False, slow_mo=300)
    # creates the new page
    page = browser.new_page()
    page.set_viewport_size({"width": 527, "height": 480})
    # returns the main source response
    # @param url to navigate page to
    page.goto(url)
    # Pauses script execution
    page.screenshot(path="debug.png")
    page.pause()
    # Close browser
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
