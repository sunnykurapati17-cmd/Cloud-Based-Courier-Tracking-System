from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "courier_tracking_secret"

DB = "courier.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS couriers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tracking_id TEXT UNIQUE NOT NULL,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            current_location TEXT NOT NULL,
            status TEXT NOT NULL,
            expected_date TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM couriers").fetchone()[0]
    if count == 0:
        demo = [
            ("CT1001", "Arun Kumar", "Priya Sharma", "Chennai", "Bengaluru",
             "Chennai Hub", "In Transit", "2026-10-12"),
            ("CT1002", "Rahul", "Anitha", "Hyderabad", "Chennai",
             "Chennai Delivery Center", "Out for Delivery", "2026-10-08"),
            ("CT1003", "Kiran", "Vijay", "Mumbai", "Delhi",
             "Mumbai Sorting Center", "Processing", "2026-10-14")
        ]
        for item in demo:
            conn.execute("""
                INSERT INTO couriers
                (tracking_id, sender, receiver, origin, destination,
                 current_location, status, expected_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (*item, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/track", methods=["POST"])
def track():
    tracking_id = request.form.get("tracking_id", "").strip().upper()
    conn = get_db()
    courier = conn.execute(
        "SELECT * FROM couriers WHERE tracking_id = ?", (tracking_id,)
    ).fetchone()
    conn.close()

    if courier:
        return render_template("tracking.html", courier=courier)
    flash("Tracking ID not found. Try CT1001, CT1002 or CT1003.")
    return redirect(url_for("home"))

@app.route("/admin")
def admin():
    conn = get_db()
    couriers = conn.execute("SELECT * FROM couriers ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", couriers=couriers)

@app.route("/admin/add", methods=["POST"])
def add_courier():
    data = request.form
    try:
        conn = get_db()
        conn.execute("""
            INSERT INTO couriers
            (tracking_id, sender, receiver, origin, destination,
             current_location, status, expected_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["tracking_id"].strip().upper(),
            data["sender"], data["receiver"], data["origin"],
            data["destination"], data["current_location"],
            data["status"], data["expected_date"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        flash("Courier added successfully.")
    except sqlite3.IntegrityError:
        flash("Tracking ID already exists.")
    return redirect(url_for("admin"))

@app.route("/admin/update/<int:courier_id>", methods=["POST"])
def update_courier(courier_id):
    data = request.form
    conn = get_db()
    conn.execute("""
        UPDATE couriers
        SET current_location = ?, status = ?, expected_date = ?
        WHERE id = ?
    """, (data["current_location"], data["status"],
          data["expected_date"], courier_id))
    conn.commit()
    conn.close()
    flash("Courier status updated.")
    return redirect(url_for("admin"))

@app.route("/admin/delete/<int:courier_id>", methods=["POST"])
def delete_courier(courier_id):
    conn = get_db()
    conn.execute("DELETE FROM couriers WHERE id = ?", (courier_id,))
    conn.commit()
    conn.close()
    flash("Courier deleted.")
    return redirect(url_for("admin"))

@app.route("/api/track/<tracking_id>")
def api_track(tracking_id):
    conn = get_db()
    courier = conn.execute(
        "SELECT * FROM couriers WHERE tracking_id = ?",
        (tracking_id.upper(),)
    ).fetchone()
    conn.close()

    if not courier:
        return jsonify({"error": "Tracking ID not found"}), 404
    return jsonify(dict(courier))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
