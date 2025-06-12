# app.py
from flask import Flask, request, redirect, render_template, session
import sqlite3

app = Flask(__name__)
app.secret_key = "s3cr3t"

FLAG = open("flag.txt").read().strip()

def get_db():
    conn = sqlite3.connect("vuln.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    if "user" in session:
        user = session["user"]
        if user == "admin":
            return render_template("home.html", user=user, flag=FLAG)
        return render_template("home.html", user=user)
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        cur = get_db().execute(
            f"SELECT * FROM users WHERE username = '{u}' AND password = '{p}'"
        )
        if cur.fetchone():
            session["user"] = u
            return redirect("/")
        error = "로그인 실패"
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        db = get_db()
        db.execute(
            f"INSERT INTO users (username,password) VALUES ('{u}','{p}')"
        )
        db.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
