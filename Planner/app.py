import sqlite3

from flask import Flask, session, render_template, request, flash, g, redirect, url_for

app = Flask(__name__)
app.secret_key = "jfd0sfid09foifjds0fjfohsd9jdsfn"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def index():
    email = request.form["email"]
    password = request.form["password"]

    for user in get_users():
        print(user)
        if user[3] == email and user[4] == password:
            session["user"] = user
            return redirect(url_for("calendar"))
            flash("Welcome " + user[1])

    return render_template("index.html")


@app.route("/logout")
def logout():
    return render_template("index.html")


@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/calendar")
def calendar():
    return render_template("Planner.html")


@app.route("/cadastro", methods=["POST"])
def sign_in():
    name = request.form["name"]
    nickname = request.form["nickname"]
    birthday = request.form["birthday"]
    email = request.form["email"]
    password = request.form["password"]
    data = get_db()
    cursor = data.cursor()
    query1 = "INSERT INTO user VALUES('{n}','{nick}', '{bday}', '{email}', '{password}')".format(n=name, nick=nickname, bday=birthday, email=email, password=password)
    cursor.execute(query1)
    data.commit()
    return render_template("index.html")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('Planner.db')
    return db


def get_users():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('Planner.db')
        cursor = db.cursor()
        query1 = "SELECT * FROM user"
        cursor.execute(query1)
        all_data = cursor.fetchall()
    return all_data


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run()