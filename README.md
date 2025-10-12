# Task receipts

---

Organize your day by printing your tasks and making productivity rewarding

## About this project

---

This project turns your daily tasks into real printed receipts using a
thermal printer.
It's built with Flask for the web interface, Playwright for HTML rendering,
Pillow for image processing, and python-escpos for printing.
It started as an experiment to learn how to combine web rendering with physical
output, and it's evolving into a gamified productivity tool.

## How it works

---

1. Flask serves an HTML page (currently a static "Hello world").
2. Playwright loads the page and takes a screenshot of it.
3. Pillow converts the screenshot to a black-and-white image.
4. python-escpos sends that image to the printer

## Current features

---

- Playwright can render HTML to PNG
- Pillow converts and prints images
- Receipt desing in process

## Next steps

---

- [ ] Design the real receipt layout
- [ ] Add task input fields and dynamic data
- [ ] Reuse Playwright browser for faster prints

## Setup

---

1. Clone this repo
2. Create a virtual environment
3. Install dependencies:
   ```bash
   pip install flask playwright pillow python-escpos
   playwright install chromium
   ```
