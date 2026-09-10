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
    

@app.route("/contacts/<contact_id>")
def contacts_view(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("show.html", contact=contact)


@app.route("/contacts/<contact_id>/edit", methods=["GET"])
def contacts_edit_get(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("edit.html", contact=contact)


@app.route("/contacts/<contact_id>/edit", methods=["POST"])
def contacts_edit_post(contact_id=0):
    c = Contact.find(contact_id)
    c.update(
        request.form["first_name"],
        request.form["last_name"],
        request.form["phone"],
        request.form["email"]
    )
    if c.save():
        flash("Updated contact")
        return redirect("/contacts/" + str(contact_id))
    else:
        return render_template("edit.html", contact=c)