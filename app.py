from datetime import datetime
from pathlib import Path

from escpos.printer import Usb
from flask import Flask, render_template, request
from PIL import Image
from playwright.sync_api import Playwright, sync_playwright

app = Flask(__name__)

path = Path("templates/index.html").resolve()
url = path.as_uri()
css_path = Path("static/style.css").resolve()


def run(playwright: Playwright):
    # set the browser to use:
    chromium = playwright.chromium
    # returns the browser instance
    browser = chromium.launch(headless=False)
    # creates the new page
    page = browser.new_page()
    page.set_viewport_size({"width": 600, "height": 800})
    # returns the main source response
    # @param url to navigate page to
    page.goto(url)
    page.add_style_tag(path=css_path)
    # Pauses script execution
    page.pause()
    page.screenshot(path="debug.png", full_page=True)
    # Close browser
    browser.close()


@app.route("/create_receipt/<id>", methods=["GET", "POST"])
def create_receipt(id):
    if request.method == "POST":
        if "submit_button" in request.form:
            date_str = None
            has_date = None
            has_task = None
            task_name = None
            has_priority = None
            priority_level = None

            if "task_name" in request.form:
                task_name = request.form.get("task_name")
                has_task = True

            if "selected_date" in request.form:
                date_str = request.form.get("selected_date")
                has_date = True

            if "priority" in request.form:
                priority_level = request.form.get("priority")
                has_priority = True

            return render_template(
                "index.html",
                date=date_str,
                has_date=has_date,
                task_name=task_name,
                has_task=has_task,
                priority=priority_level,
                has_priority=has_priority,
            )

        return render_template("index.html")

@app.route("/print_receipt/<id>"), methods["GET", "POST"])
def print_receipt(id):
    if "print_receipt" in request.form:
        with sync_playwright() as playwright:
            run(playwright)
        image = None

        with Image.open("debug.png") as im:       
        image = im.convert(mode="1", dither=Image.FLOYDSTEINBERG)
        
        p = Usb(0x0FE6, 0x811E)
        p.image(image)
        p.cut()
    return
