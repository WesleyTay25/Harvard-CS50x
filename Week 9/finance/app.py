import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    userID = session.get("user_id")
    portfolio = db.execute("SELECT stock, shares FROM stocks WHERE usernameid = ?", userID)
    ownedstocks = db.execute("SELECT stock FROM stocks WHERE usernameid = ?", userID)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", userID)

    stocks_price = []
    for stock in ownedstocks:
        stocks_price.append((lookup(stock["stock"]))["price"])

    for i in range(len(portfolio)):
        portfolio[i]['price'] = stocks_price[i]

    total_price = 0
    for i in range(len(portfolio)):
        total_price += (stocks_price[i] * portfolio[i]["shares"])

    return render_template("index.html", portfolio=portfolio, cash=cash[0]["cash"], total_price=total_price)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    userID = session.get("user_id")
    if request.method == "POST":
        stock = request.form.get("symbol")

        if not stock:
            return apology("Please Input Stock", 400)

        shares = (request.form.get("shares"))

        if not shares:
            return apology("Please Input Number of Shares", 400)

        try:
            shares = int(shares)
        except ValueError:
            return apology("Invalid Input", 400)

        if shares < 0:
            return apology("Number of shares cannot be below zero", 400)
        if shares == 0:
            return apology("Number of shares bought cannot be zero", 400)

        data = lookup(stock)

        if not data:
            return apology("Stock cannot be found", 400)

        stockprice = float(data["price"])
        stocksymbol = data["symbol"]
        cash_dict = db.execute("SELECT cash FROM users WHERE id = ?", session.get("user_id"))
        cash = (cash_dict[0]["cash"])
        cost = round((shares * stockprice), 2)
        new_cash = round((cash - cost), 2)

        if cost > cash:
            return apology("Insufficient funds", 400)

        ownedstocks = db.execute(
            "SELECT stock FROM stocks WHERE usernameid = ? AND stock = ?", userID, stocksymbol)
        if ownedstocks:
            ownedshares = db.execute(
                "SELECT shares FROM stocks WHERE usernameid = ? AND stock = ?", userID, stocksymbol)
            ownedshares = float(ownedshares[0]["shares"])
            totalshares = round((shares + ownedshares), 2)
            db.execute("UPDATE stocks SET shares = ? WHERE usernameid = ? AND stock = ?",
                       totalshares, userID, stocksymbol)
        else:
            db.execute("INSERT INTO stocks (usernameid, stock, shares) VALUES (?, ?, ?)",
                       userID, stocksymbol, shares)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, userID)
        db.execute("INSERT INTO history (usernameid, stock, shares, price) VALUES (?,?,?,?)",
                   userID, stocksymbol, shares, stockprice)
        flash("Purchase Sucess!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    userID = session.get("user_id")
    history = db.execute(
        "SELECT stock, shares, price, time FROM history WHERE usernameid = ?", userID)
    print(history)
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stock = request.form.get("symbol")

        if not stock:
            return apology("Please Input Stock", 400)

        data = lookup(stock)

        if not data:
            return apology("Not a Stock", 400)

        stockname = data["name"]
        stockprice = usd(data["price"])
        stocksymbol = data["symbol"]

        return render_template("quoted.html", name=stockname, price=stockprice, symbol=stocksymbol)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            return apology("Please enter a username")

        password = request.form.get("password")
        if not password:
            return apology("Please enter a password")

        confirm = request.form.get("confirmation")
        if not confirm:
            return apology("Please confirm password")

        if password != confirm:
            return apology("Passwords do not match")

        try:
            passwordhash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, passwordhash)
        except ValueError:
            return apology("Please enter Unique Username")
        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stockuserID = session.get("user_id")"""
    userID = session.get("user_id")
    stocks_dict = db.execute("SELECT stock FROM stocks WHERE usernameid = ?", userID)

    if request.method == "POST":
        stocks = []
        for stock in stocks_dict:
            stocks.append(stock["stock"])

        symbol = request.form.get("symbol")

        if not symbol:
            return apology("Enter a symbol", 400)

        if symbol not in stocks:
            return apology("You do not have this stock", 400)

        shares = int(request.form.get("shares"))

        if not shares:
            return apology("Enter amount of shares to sell", 400)
        if shares == 0 or shares < 0:
            return apology("Enter a valid number", 400)

        ownedshares = db.execute(
            "SELECT stock, shares FROM stocks WHERE usernameid = ? AND stock = ?", userID, symbol)
        ownedshares = int(ownedshares[0]["shares"])
        if shares > ownedshares:
            return apology("Insufficient shares", 400)

        cash = db.execute("SELECT cash FROM users WHERE id = ?", userID)
        cash = float(cash[0]["cash"])
        price = float((lookup(symbol))["price"])
        total = round((cash + (price * shares)), 2)
        shares_left = ownedshares - shares

        if shares == ownedshares:
            db.execute("DELETE FROM stocks WHERE usernameid = ? AND stock = ?", userID, symbol)
        else:
            db.execute("UPDATE stocks SET shares = ? WHERE usernameid = ? AND stock = ?",
                       shares_left, userID, symbol)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", total, userID)
        db.execute("INSERT INTO history (usernameid, stock, shares, price) VALUES (?, ?, ?, ?)",
                   userID, symbol, (shares * -1), round(price, 2))
        flash("Sell Sucess!")
        return redirect("/")

    return render_template("sell.html", stocks=stocks_dict)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    userID = session.get("user_id")
    cash = float(db.execute("SELECT cash from users WHERE id = ?", userID)[0]["cash"])

    if request.method == "POST":
        edit = request.form.get("edit")

        if not edit:
            return apology("Enter edit amount", 400)

        try:
            edit = float(edit)
            if edit == 0 or edit < 0:
                return apology("Input valid amount", 400)
        except ValueError:
            return apology("Input a number", 400)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", edit, userID)
        flash("Edited!")
        return redirect("/")

    return render_template("edit.html", cash=cash)
