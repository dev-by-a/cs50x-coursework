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
    user_id = session["user_id"]

    holdings = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id
    )

    stocks = []
    stock_total = 0
    for holding in holdings:
        quote = lookup(holding["symbol"])
        value = quote["price"] * holding["total_shares"]
        stock_total += value
        stocks.append({
            "symbol": holding["symbol"],
            "shares": holding["total_shares"],
            "price": quote["price"],
            "total": value
        })

    rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = rows[0]["cash"]
    grand_total = cash + stock_total

    return render_template("index.html", stocks=stocks, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        qoute = lookup(symbol)
        if qoute is None:
            return apology("invalid symbol", 400)

        shares = request.form.get("shares")
        if not shares:
            return apology("must provide shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if shares < 1:
            return apology("shares must be a positive integer", 400)

        cost = qoute["price"] * shares

        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = rows[0]["cash"]

        if cost > cash:
            return apology("can't afford", 400)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, qoute["symbol"], shares, qoute["price"]
        )

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        user_id
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

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
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        qoute = lookup(symbol)
        if qoute is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", name=qoute["name"], symbol=qoute["symbol"], price=qoute["price"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        existing = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(existing) > 0:
            return apology("username already exists", 400)

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation:
            return apology("must provide password and confirmation", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        hash = generate_password_hash(password)
        new_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        session["user_id"] = new_id
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must select a stock", 400)

        shares = request.form.get("shares")
        if not shares:
            return apology("must provide shares", 400)
        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if shares < 1:
            return apology("shares must be a positive integer", 400)

        owned = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ?",
            user_id, symbol
        )
        total_shares = owned[0]["total_shares"]

        if total_shares is None or shares > total_shares:
            return apology("too many shares", 400)

        quote = lookup(symbol)
        sale_value = quote["price"] * shares

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            user_id, symbol, -shares, quote["price"]
        )

        return redirect("/")
    else:
        symbols = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
            user_id
        )
        symbols = [row["symbol"] for row in symbols]
        return render_template("sell.html", symbols=symbols)
