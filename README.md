# Task Receipts

**Turn your daily tasks into real printed receipts on a thermal printer, so the thing you track is physical, not another app on your phone.**

> **Status:** Work in progress and a learning project. You can fill in a task, preview
> it as a receipt and print it. Saving tasks to a SQLite database (with a task list
> and an htmx add-task form) is in progress on the
> [`db-migration`](../../tree/db-migration) branch.

## How it works

1. You fill in a form with a task name, a deadline and a priority. Flask validates
   the input and keeps the task in the session.
2. Flask renders the task as a receipt page.
3. When you print, Playwright opens that page in headless Chromium and takes a
   screenshot of it.
4. Pillow turns the screenshot into a 1-bit (black and white) image with
   Floyd–Steinberg dithering, the format a thermal printer understands.
5. python-escpos sends the image to the printer over USB and cuts the paper. If
   the printer is off, busy or unplugged, the page tells you.

Receipts are drawn from real HTML and CSS, so you can change the design by editing
`static/style.css` instead of being limited to the printer's built-in text commands.

Design decisions, including ones I later changed, are recorded as
[Architecture Decision Records](docs/adr/).

## Stack

Flask · Playwright (Chromium) · Pillow · python-escpos + pyusb

## Setup

You need Python 3 and a USB thermal printer that speaks ESC/POS.

```bash
git clone git@github.com:Jaairg/task-receipts.git
cd task-receipts

python -m venv .venv
source .venv/bin/activate

pip install flask playwright pillow python-escpos pyusb python-dotenv
playwright install chromium

# Generate a secret key (it signs Flask sessions). .env is gitignored.
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" > .env

flask --app app run
```

Then open <http://127.0.0.1:5000/create_receipt>.

> **Printer IDs:** the USB vendor and product IDs are hardcoded in
> `send_to_printer()` in `app.py` (`Usb(0x0FE6, 0x811E)`). Change them to your
> printer's IDs, which you can find with `lsusb`.

## Next steps

- [x] Real receipt layout and task input fields
- [x] Validate the form and handle printer errors
- [ ] Store tasks in SQLite with a task list (in progress on `db-migration`)
- [ ] Detect the printer automatically instead of hardcoding USB IDs
- [ ] Reuse the Playwright browser between prints so printing is faster
