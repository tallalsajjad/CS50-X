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
    user_id = session["user_id"]

    # Get user's current cash
    user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]
    cash = user["cash"]

    # Get user's current stock holdings (grouped by symbol)
    holdings = db.execute("""
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """, user_id)

    total_stock_value = 0
    portfolio = []

    for holding in holdings:
        symbol = holding["symbol"]
        shares = holding["total_shares"]

        stock = lookup(symbol)
        if stock:
            price = stock["price"]
            total = price * shares
            total_stock_value += total

            portfolio.append({
                "symbol": symbol,
                "name": stock["name"],
                "shares": shares,
                "price": price,
                "total": total
            })

    grand_total = total_stock_value + cash

    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    if request.method == "POST":
        stock_symbol = request.form.get("symbol")
        stock = lookup(stock_symbol)
        if not stock_symbol or stock is None:
            return apology("Missing symbol")
        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Invalid number of shares")

        shares = int(shares)
        cost = stock["price"] * shares

        # Check user's cash
        user_id = session["user_id"]
        user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]
        if cost > user["cash"]:
            return apology("Not enough cash")

        # Update database: deduct cash and record purchase
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, user_id)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
            user_id, stock["symbol"], shares, stock["price"], "buy"
        )

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user = session["user_id"]
    history = db.execute(
        "SELECT price, shares, type, timestamp, symbol FROM transactions WHERE user_id = ?", user)
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
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol not found")
        stock = lookup(symbol)
        if stock is None:
            return apology("Not available")
        return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'GET':
        return render_template("register.html")
    if request.method == 'POST':
        if not request.form.get("username"):
            return apology("INVALID USERNAME")
        if not request.form.get("password"):
            return apology("INVALID PASSWORD")
        if not request.form.get("confirmation"):
            return apology("Required confirmation")
        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("Check Password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) > 0:
            return apology("Username already exists.")
        password = request.form.get("password")
        hash_password = generate_password_hash(password)
        result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                            request.form.get("username"), hash_password)
        session["user_id"] = result
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        # Query the database for stocks the user owns
        rows = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = ?", user_id)
        return render_template("sell.html", stocks=rows)

    symbol = request.form.get("symbol")
    if not symbol:
        return apology("Missing symbol")

    stock = lookup(symbol)
    if stock is None:
        return apology("Missing stock")

    user = session["user_id"]

    shares_result = db.execute(
        "SELECT SUM(shares) AS total_shares FROM transactions WHERE symbol = ? AND user_id = ?", symbol, user)[0]
    shares_own = shares_result["total_shares"]

    if not shares_own or shares_own <= 0:
        return apology("You don't have this stock")

    shares = request.form.get("shares")
    if not shares or not shares.isdigit():
        return apology("Invalid number of shares")

    shares_to_sell = int(shares)
    if shares_to_sell <= 0:
        return apology("Shares must be positive")
    if shares_to_sell > shares_own:
        return apology("You don't have enough shares")

    price = stock["price"]
    total = price * shares_to_sell

    db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total, user)
    db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, ?)",
               user, symbol, -shares_to_sell, price, "sell")

    return redirect("/")
