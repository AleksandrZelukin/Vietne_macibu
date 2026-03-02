import sqlite3
from flask import Flask, render_template, request, redirect, session
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "school_secret_key"


def get_user(username):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user


@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username)

        if user and check_password_hash(user[2], password):
            session["user"] = username
            session["role"] = user[3]
            return redirect("/dashboard")
        else:
            error = "Nepareiza lietotājvārds vai parole."

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        user=session["user"],
        role=session["role"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)