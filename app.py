from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize SQLite DB
def init_db():
    conn = sqlite3.connect("donors.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS donors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            place TEXT,
            email TEXT,
            phone TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Donation submission
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    name = data.get("name")
    place = data.get("place")
    email = data.get("email")
    phone = data.get("phone")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert into DB
    conn = sqlite3.connect("donors.db")
    c = conn.cursor()
    c.execute("INSERT INTO donors (name, place, email, phone, date) VALUES (?, ?, ?, ?, ?)",
              (name, place, email, phone, date))
    conn.commit()
    conn.close()

    # Response message
    thank_you = f"Dear {name} from {place}, your seva has been received with love. A confirmation has been sent to {email}."
    return jsonify({"status":"success", "message": thank_you})

if __name__ == "__main__":
    app.run(debug=True)
