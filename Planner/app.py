from flask import Flask, request, session, redirect, url_for, render_template
from database import engine
from sqlalchemy import text
from user import load_users_from_db, create_users_from_db
from event import create_events_from_db, load_events_from_db, delete_event_by_id
import connexion

app = Flask(__name__)
app.secret_key = "jfd0sfid09foifjds0fjfohsd9jdsfn"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def index():
    email = request.form["email"]
    password = request.form["password"]

    for user in load_users_from_db():
        print(user)
        if user["usuario_email"] == email and user["usuario_senha"] == password:
            session["user"] = user
            return redirect(url_for("calendar"))

    return render_template("index.html")


@app.route("/logout")
def logout():
    return render_template("index.html")

@app.route("/createevent")
def createevent():
    return render_template("createevent.html")

@app.route("/deleteevent")
def deleteevent():
    return render_template("deleteevent.html")

@app.route("/listevents")
def listevents():
    events = load_events_from_db()
    return render_template("listevents.html", events = events)


@app.route("/signup")
def sign_up():
    return render_template("signup.html")


@app.route("/calendar")
def calendar():
    return render_template("Planner.html")

@app.route("/cadastro", methods=["POST"])
def sign_in():
    user_id = request.form["user_id"]
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    create_users_from_db(user_id, name, email, password, 0)
    return render_template("index.html")

@app.route("/new event", methods=["POST"])
def new_event():
    event_id = request.form["event_id"]
    title = request.form["title"]
    description = request.form["description"]
    date = request.form["date"]
    user_id = request.form["user_id"]
    create_events_from_db(event_id, title, description, date, 0, user_id)
    return render_template("Planner.html")

@app.route("/delete event", methods=["POST"])
def delete_event():
    event_id = request.form["event_id"]
    delete_event_by_id(event_id)
    return render_template("Planner.html")

if __name__ == '__main__':
    app.run()