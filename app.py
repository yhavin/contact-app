import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request

from models import Contact

load_dotenv()

Contact.load_db()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


@app.route("/")
def index():
    return redirect("/contacts")


@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    if search is not None:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()
    return render_template("index.html", contacts=contacts_set)


@app.route("/contacts/new", methods=["GET"])
def contacts_new_get():
    return render_template("new.html", contact=Contact())


@app.route("/contacts/new", methods=["POST"])
def contacts_new():
    c = Contact(
        None,
        request.form["first_name"],
        request.form["last_name"],
        request.form["phone"],
        request.form["email"]
    )
    if c.save():
        flash("Created new contact")
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=c)