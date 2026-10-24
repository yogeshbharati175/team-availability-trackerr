from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-before-deployment"
DATABASE = Path(__file__).with_name("team.db")
VALID_STATUSES = ("Available", "Busy", "Away")


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Team Member',
                status TEXT NOT NULL DEFAULT 'Away',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        count = db.execute("SELECT COUNT(*) FROM members").fetchone()[0]
        if count == 0:
            db.executemany(
                "INSERT INTO members (name, role, status) VALUES (?, ?, ?)",
                [
                    ("Aarav Patil", "Python Developer", "Available"),
                    ("Priya Sharma", "UI/UX Designer", "Busy"),
                    ("Rahul Jadhav", "Database Engineer", "Away"),
                    ("Sneha Kulkarni", "QA Engineer", "Available"),
                ],
            )


@app.route("/")
def dashboard():
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "All")
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM members").fetchone()[0]
        counts = {
            status: db.execute(
                "SELECT COUNT(*) FROM members WHERE status = ?", (status,)
            ).fetchone()[0]
            for status in VALID_STATUSES
        }

        sql = "SELECT * FROM members WHERE (name LIKE ? OR role LIKE ?)"
        params = [f"%{search}%", f"%{search}%"]
        if status_filter in VALID_STATUSES:
            sql += " AND status = ?"
            params.append(status_filter)
        sql += " ORDER BY name COLLATE NOCASE"
        members = db.execute(sql, params).fetchall()

    return render_template(
        "index.html",
        members=members,
        total=total,
        counts=counts,
        search=search,
        status_filter=status_filter,
    )


@app.post("/members/add")
def add_member():
    name = request.form.get("name", "").strip()
    role = request.form.get("role", "").strip() or "Team Member"
    status = request.form.get("status", "Away")
    if not name:
        flash("Please enter a team member name.", "error")
    elif status not in VALID_STATUSES:
        flash("Please select a valid status.", "error")
    else:
        with get_db() as db:
            db.execute(
                "INSERT INTO members (name, role, status) VALUES (?, ?, ?)",
                (name, role, status),
            )
        flash(f"{name} was added to the team.", "success")
    return redirect(url_for("dashboard"))


@app.post("/members/<int:member_id>/status")
def update_status(member_id):
    status = request.form.get("status", "")
    if status not in VALID_STATUSES:
        flash("Invalid status selected.", "error")
    else:
        with get_db() as db:
            result = db.execute(
                "UPDATE members SET status = ? WHERE id = ?", (status, member_id)
            )
        if result.rowcount:
            flash("Member status updated.", "success")
        else:
            flash("Team member not found.", "error")
    return redirect(url_for("dashboard"))


@app.post("/members/<int:member_id>/delete")
def delete_member(member_id):
    with get_db() as db:
        result = db.execute("DELETE FROM members WHERE id = ?", (member_id,))
    flash("Team member deleted." if result.rowcount else "Team member not found.",
          "success" if result.rowcount else "error")
    return redirect(url_for("dashboard"))


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
else:
    # Also initialize the database when loaded by a WSGI server.
    init_db()
