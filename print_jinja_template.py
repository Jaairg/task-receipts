from escpos.printer import Usb
from flask import Flask, render_template, request, url_for
from jinja2 import Environment, FileSystemLoader
from markupsafe import escape

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("receipt.txt.j2")
app = Flask(__name__)


@app.route("/print/<id>", methods=["GET", "POST"])
def hello(id):
    if request.method == "POST":
        ticket_id = request.form.get("job_id")

        context = {
            "title": "Task 1",
            "due_date": "12/29/2025",
            "priority": "HIGH",
            "notes": "Learn Flask",
        }

        render_text = template.render(**context)

        p = Usb(0x0FE6, 0x811E)
        p.text(render_text)
        p.cut()

        return f"Would print task { ticket_id }"

    return render_template("index.html", job_id=id)


@app.route("/projects/")
def projects():
    return "Hello"
