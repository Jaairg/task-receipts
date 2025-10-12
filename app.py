from pathlib import Path

from escpos.printer import Usb
from flask import Flask, render_template, request
from PIL import Image
from playwright.sync_api import Playwright, sync_playwright

app = Flask(__name__)

path = Path("templates/index.html").resolve()
url = path.as_uri()


def run(playwright: Playwright):
    # set the browser to use:
    chromium = playwright.chromium
    # returns the browser instance
    browser = chromium.launch(headless=True)
    # creates the new page
    page = browser.new_page()
    page.set_viewport_size({"width": 527, "height": 480})
    # returns the main source response
    # @param url to navigate page to
    page.goto(url)
    # Pauses script execution
    page.screenshot(path="debug.png")
    # Close browser
    browser.close()


@app.route("/print_receipt/<id>", methods=["GET", "POST"])
def print(id):
    if request.method == "POST":

        with sync_playwright() as playwright:
            run(playwright)
        image = None

        with Image.open("debug.png") as im:
            image = im.convert(mode="1", dither=Image.FLOYDSTEINBERG)

        p = Usb(0x0FE6, 0x811E)
        p.image(image)
        p.cut()

    return render_template("index.html", job_id=id)
