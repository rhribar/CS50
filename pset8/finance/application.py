import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get info from database
    rows = db.execute("SELECT * FROM stocks WHERE user_id = :user",
                      user=session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = :user",
                      user=session["user_id"])[0]['cash']

    cash_all = cash
    stocks = []
    # Go through all data!
    for i, row in enumerate(rows):
        stock_info = lookup(row['symbol'])
        stocks.append(list((stock_info['symbol'], stock_info['name'], row['amount'],
                            stock_info['price'], round(stock_info['price'] * row['amount'], 2))))

        cash_all += stocks[i][4]

    return render_template("index.html", stocks=stocks, cash=round(cash, 2), cash_all=round(cash_all, 2))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # handle for GET
    if request.method == "GET":
        return render_template("buy.html")

    # handle for POST
    elif request.method == "POST":
        # Get values from user
        number = int(request.form.get("amount"))
        stock_symbol = lookup(request.form.get("symbol"))['symbol']

        # Check stock price and users cash
        price_share = lookup(stock_symbol)['price']
        avaliable_cash = db.execute("SELECT cash FROM users WHERE id = :user",
                                    user = session["user_id"])[0]['cash']

        # Check if user has enough cash!
        cash_left = avaliable_cash - price_share * float(number)
        if cash_left < 0:
            return apology("U broke!")

        # Check if user has this stock already
        stock = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                            user=session["user_id"], symbol=stock_symbol)

        # Insert and update interface
        if not stock:
            db.execute("INSERT INTO stocks(user_id, symbol, amount) VALUES (:user, :symbol, :amount)",
                       user=session["user_id"], symbol=stock_symbol, amount=number)
        else:
            number += stock[0]['amount']

            db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol",
                       user=session["user_id"], symbol=stock_symbol, amount=number)

        # Update user and history table
        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                    cash=cash_left, user=session["user_id"])

        db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                   user=session["user_id"], symbol=stock_symbol, amount=number, value=round(price_share*float(number)))

        flash("Stocks have been added!")

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    rows = db.execute("SELECT * FROM transactions WHERE user_id = :user",
                      user=session["user_id"])

    # pass a list of lists to the template page, template is going to iterate it to extract the data into a table
    transactions = []
    for row in rows:
        stock_info = lookup(row['symbol'])

        # create a list with all the info about the transaction and append it to a list of every stock transaction
        transactions.append(list((stock_info['symbol'], stock_info['name'], row['amount'], row['value'], row['date'])))

    # redirect user to index page
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # Handle for POST
    if request.method == "POST":

        # Check if username was submitted
        if not request.form.get("username"):
            return apology("You must provide username", 403)

        # Check if password was submitted
        elif not request.form.get("password"):
            return apology("You must provide password", 403)

        # Check database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Check if username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember the user via session
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # Handle for GET
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
        return render_template("quote.html", stock="")

    elif request.method == "POST":

        stock = lookup(request.form.get("symbol"))
        return render_template("quote.html", stock=stock)
    # return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":

        # Check if passwords match
        if request.form.get("password") != request.form.get("password_check"):
            return apology("Your passwords do not match.", 403)

        # Check if username was submitted
        elif not request.form.get("username"):
            return apology("You must provide username.", 403)

        # Check if password was submitted
        elif not request.form.get("password"):
            return apology("You must provide password.", 403)

        # Check if user is already in the database
        elif db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username")):
            return apology("Sorry this user already exists.", 403)

        # Insert user into the database
        db.execute("INSERT INTO users(username, hash) VALUES (:username, :hash)",
                   username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Check for users table
        rows=db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Get user id and start a session
        session["user_id"] = rows[0]["id"]
        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # handle for GET
    if request.method == "GET":
        rows = db.execute("SELECT symbol, amount FROM stocks WHERE user_id = :user",
                            user=session["user_id"])
        stocks = {}
        for row in rows:
            stocks[row['symbol']] = row['amount']

        return render_template("sell.html", stocks=stocks)

    # handle for POST
    elif request.method == "POST":
        # Get values from user
        amount = request.form.get("amount")
        if amount is not None:
            amount = int(request.form.get("amount"))

        symbol = request.form.get("symbol")
        price = lookup(symbol)["price"]
        value = round(price*float(amount))

        # Updating the stocks table
        amount_before = db.execute("SELECT amount FROM stocks WHERE user_id = :user AND symbol = :symbol",
                                   symbol=symbol, user=session["user_id"])[0]['amount']
        amount_after = amount_before - amount

        # Delete stocks from table if we do not have anymore stocks
        if amount_after == 0:
            db.execute("DELETE FROM stocks WHERE user_id = :user AND symbol = :symbol",
                       symbol=symbol, user=session["user_id"])

        # Fail-safe if the user wants to sell more stocks than he own them
        elif amount_after < 0:
            return apology("That's more than the stocks you own")

        # sell the stocks and update the table
        else:
            db.execute("UPDATE stocks SET amount = :amount WHERE user_id = :user AND symbol = :symbol",
                       symbol=symbol, user=session["user_id"], amount=amount_after)

        # refresh user money
        cash = db.execute("SELECT cash FROM users WHERE id = :user",
                          user=session["user_id"])[0]['cash']
        cash_after = cash + price * float(amount)

        db.execute("UPDATE users SET cash = :cash WHERE id = :user",
                   cash=cash_after, user=session["user_id"])

        # Update history table
        db.execute("INSERT INTO transactions(user_id, symbol, amount, value) VALUES (:user, :symbol, :amount, :value)",
                   user=session["user_id"], symbol=symbol, amount=-amount, value=value)

        flash("Stocks have been sold!")
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
