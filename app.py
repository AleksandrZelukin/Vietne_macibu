import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "school_secret_key"


def query_db(query, args=(), one=False):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    c.execute(query, args)
    rv = c.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = query_db(
            "SELECT * FROM users WHERE username = ?",
            (request.form["username"],),
            one=True
        )

        if user and check_password_hash(user[2], request.form["password"]):
            session["user_id"] = user[0]
            session["role"] = user[3]
            return redirect("/dashboard")
        else:
            error = "Nepareizs lietotājvārds vai parole"

    return render_template("login_lv.html", error=error)

@app.route("/lang/<code>")
def change_language(code):
    if code in ["lv", "ru"]:
        session["lang"] = code
    return redirect(request.referrer or "/")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    if session["role"] == "student":
        student = query_db(
            "SELECT id, full_name FROM students WHERE user_id = ?",
            (session["user_id"],),
            one=True
        )

        grades = query_db("""
            SELECT subjects.name, grades.grade, grades.date
            FROM grades
            JOIN subjects ON grades.subject_id = subjects.id
            WHERE grades.student_id = ?
        """, (student[0],))

        avg = query_db(
            "SELECT ROUND(AVG(grade),2) FROM grades WHERE student_id = ?",
            (student[0],),
            one=True
        )[0]

        return render_template(
            "student_dashboard_lv.html",
            name=student[1],
            grades=grades,
            average=avg
        )

    # ===== teacher =====
    students = query_db("SELECT id, full_name FROM students")
    subjects = query_db("SELECT id, name FROM subjects")

    return render_template(
        "teacher_dashboard_lv.html",
        students=students,
        subjects=subjects
    )


@app.route("/add_grade", methods=["POST"])
def add_grade():
    if session.get("role") != "teacher":
        return redirect("/")

    query_db("""
        INSERT INTO grades (student_id, subject_id, grade, date)
        VALUES (?, ?, ?, DATE('now'))
    """, (
        request.form["student"],
        request.form["subject"],
        request.form["grade"]
    ))

    return redirect("/dashboard")

@app.route("/class_journal")
def class_journal():
    if session.get("role") != "teacher":
        return redirect("/")

    data = query_db("""
        SELECT s.full_name, s.class, sub.name, g.grade, g.date
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN subjects sub ON g.subject_id = sub.id
        ORDER BY s.class, s.full_name
    """)

    return render_template("class_journal_lv.html", data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)