from datetime import datetime
from pathlib import Path

import io
import usb.core
from escpos.printer import Usb
from escpos.exceptions import USBNotFoundError
from flask import Flask, flash, redirect, render_template, request, session, url_for
from PIL import Image
from playwright.sync_api import Playwright, sync_playwright

app = Flask(__name__)

app.secret_key = "282801837c6b9242db2897a776f02807f4de186fd133801114fbe137435ab604"

css_path = Path("static/style.css").resolve()

def run(playwright: Playwright):
    # set the browser to use:
    chromium = playwright.chromium
    browser = chromium.launch() # returns the browser instance
    cookie_header = request.cookies.get("session")

    context = browser.new_context()
    context.add_cookies([
        {
            'name': 'session',
            'value': cookie_header,
            'domain': '127.0.0.1',
            'path': '/',
            'httpOnly': True,
            'sameSite': 'Lax'
        }
    ])
    # creates the new page
    page = context.new_page()
    page.set_viewport_size({"width": 600, "height": 800})
    # returns the main source response
    # @param url to navigate page to
    page.goto(url_for("print_receipt", _external=True))
    page.add_style_tag(path=css_path)

    screenshot_bytes = page.screenshot()

    context.close()
    # Close browser
    browser.close()

    return screenshot_bytes

@app.route("/create_receipt", methods=["GET", "POST"])
def create_receipt():
    if request.method == "POST":
        if "save_button" in request.form:

            if "task_name" in request.form:
                session["task_name"] = request.form.get("task_name")

            if "deadline_date" in request.form:
                session["deadline_date"] = request.form.get("deadline_date")

            if "priority_level" in request.form:
                session["priority_level"] = request.form.get("priority_level")
            
            return redirect(url_for("print_receipt"))
    return render_template("index.html", show_save_button=True)


@app.route("/print_receipt", methods=["GET", "POST"])
def print_receipt():

    is_print_submission = request.method == "POST" and "print_receipt_button" in request.form
    if not is_print_submission:
        return render_receipt_page()

    missing_fields = get_session_missing_fields()

    if missing_fields:
        return redirect(url_for("create_receipt"))

    image = generate_receipt_image()
    
    try:
        send_to_printer(image)
    except USBNotFoundError:
        app.logger.exception("Printer not found")
        flash("Printer not found: check that it's on and connected")
    except usb.core.USBError as e:
        if e.errno == 16:
            app.logger.exception("Resource busy")
            flash("Printer error: try printing one receipt at a time")
        elif e.errno == 19:
            app.logger.exception("Device disconnected")
            flash("Printer connection error: device may have been disconnected")

    return render_receipt_page()

def get_session_missing_fields():
    missing_fields = []
    
    if not session.get("task_name"):
        missing_fields.append("task_name")
    if not session.get("deadline_date"):
        missing_fields.append("deadline_date")
    if not session.get("priority_level"):
        missing_fields.append("priority_level")

    return missing_fields  

def render_receipt_page():
    return render_template(
        "index.html",
        task_name=session.get("task_name"),
        deadline_date=session.get("deadline_date"),
        priority_level=session.get("priority_level"),
        ready_to_print=True,
    )

def generate_receipt_image():
    with sync_playwright() as playwright:
        screenshot_bytes = run(playwright)

    image_stream = io.BytesIO(screenshot_bytes)

    with Image.open(image_stream) as im:
        image = im.convert(mode="1", dither=Image.FLOYDSTEINBERG)

    return image

def send_to_printer(image):
    printer = Usb(0x0FE6, 0x811E)

    try:
        printer.image(image)
        printer.cut()
    finally:
        printer.close()
