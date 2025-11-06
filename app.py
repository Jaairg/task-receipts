from datetime import datetime
from pathlib import Path

from escpos.printer import Usb
from flask import Flask, redirect, render_template, request, session, url_for
from PIL import Image
from playwright.sync_api import Playwright, sync_playwright

app = Flask(__name__)
app.secret_key = "282801837c6b9242db2897a776f02807f4de186fd133801114fbe137435ab604"
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
    page.goto(url_for("print_receipt", _external=True))
    page.add_style_tag(path=css_path)
    # Pauses script execution
    page.pause()
    page.screenshot(path="debug.png", full_page=True)
    # Close browser
    browser.close()


date_str = None
has_date = None
has_task = None
task_name = None
has_priority = None
priority_level = None


@app.route("/create_receipt", methods=["GET", "POST"])
def create_receipt():
    if request.method == "POST":
        if "submit_button" in request.form:

            if "task_name" in request.form:
                session["task_name"] = request.form.get("task_name")
                session["has_task"] = True

            if "selected_date" in request.form:
                session["date_str"] = request.form.get("selected_date")
                session["has_date"] = True

            if "priority" in request.form:
                session["priority_level"] = request.form.get("priority")
                session["has_priority"] = True
            return render_template(
                "index.html",
                date=session.get("date_str"),
                has_date=session.get("has_date"),
                task_name=session.get("task_name"),
                has_task=session.get("has_task"),
                priority=session.get("priority_level"),
                has_priority=session.get("has_priority"),
            )

        if "print_receipt" in request.form:
            return redirect("/print_receipt")
        return render_template("index.html")
    return render_template("index.html")


@app.route("/print_receipt", methods=["GET", "POST"])
def print_receipt():
    if "print_receipt" in request.form:
        with sync_playwright() as playwright:
            run(playwright)
        image = None

        with Image.open("debug.png") as im:
            image = im.convert(mode="1", dither=Image.FLOYDSTEINBERG)

        p = Usb(0x0FE6, 0x811E)
        p.image(image)
        p.cut()

    return render_template(
        "index.html",
        date=session.get("date_str"),
        has_date=session.get("has_date"),
        task_name=session.get("task_name"),
        has_task=session.get("has_task"),
        priority=session.get("priority_level"),
        has_priority=session.get("has_priority"),
    )
