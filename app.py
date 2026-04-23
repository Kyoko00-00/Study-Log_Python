import os, json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
# データの保存先
SAVE_FILE = "study_log.json"
# 試験日（自分の目標に合わせて変更してください）
EXAM_DATE = datetime(2026, 10, 18)

def load_logs():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.route("/")
def index():
    logs = load_logs()
    # 試験日までのカウントダウン
    days_left = (EXAM_DATE - datetime.now()).days
    # 新しい順に表示
    return render_template("index.html", days_left=days_left, logs=reversed(logs))

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

if __name__ == "__main__":
    app.run(debug=True)