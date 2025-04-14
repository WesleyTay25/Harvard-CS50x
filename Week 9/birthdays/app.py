import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return redirect("/")

        name = name.capitalize()
        birthday = request.form.get("birthday") #yyyy-mm-dd
        if not birthday:
            return redirect("/")

        birthday = birthday.split("-")
        year = int(birthday[0])
        month = int(birthday[1])
        day = int(birthday[2])
        db.execute("INSERT INTO birthdays (name, month, day, year) VALUES(?,?,?,?)", name, month, day, year)
        # TODO: Add the user's entry into the database

        return redirect("/")

    else:
        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)

@app.route("/remove", methods=["GET", "POST"])
def remove():
    if request.method == "POST":
        removeid = request.form.get("remove")
        if not removeid:
            return redirect("/")
        db.execute("DELETE FROM birthdays WHERE id = ?", removeid)
        return redirect("/")

