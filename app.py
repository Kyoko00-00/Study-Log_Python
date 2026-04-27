import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

SAVE_FILE = "study_log.json"
CONFIG_FILE = "config.json"
DEFAULT_EXAM_DATE = "2026-10-18"

def load_logs():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_exam_date():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            return datetime.strptime(config.get("exam_date", DEFAULT_EXAM_DATE), "%Y-%m-%d")
    return datetime.strptime(DEFAULT_EXAM_DATE, "%Y-%m-%d")

@app.route("/")
def index():
    logs = load_logs()
    exam_date = get_exam_date()
    delta = exam_date - datetime.now()
    return render_template(
        "index.html",
        days_left=delta.days,
        logs=reversed(logs),
        exam_date=exam_date.strftime("%Y-%m-%d")
    )

@app.route("/add", methods=["POST"])
def add_log():
    new_data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "subject": request.form.get("subject"),
        "hours": request.form.get("hours"),
        "memo": request.form.get("memo")
    }
    logs = load_logs()
    logs.append(new_data)
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    return redirect(url_for("index"))

@app.route("/update_config", methods=["POST"])
def update_config():
    new_date = request.form.get("exam_date")
    if new_date:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"exam_date": new_date}, f, ensure_ascii=False, indent=2)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)