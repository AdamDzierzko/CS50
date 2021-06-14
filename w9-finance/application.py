import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import datetime

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

    # get users data from stock tabel
    row = db.execute("SELECT * FROM stock WHERE owner_id = ?", session["user_id"])
    l =  len(row)

    # user saldo
    saldo = 0

    # list of dictionries with data of shares in user portfolio
    tab = []

    # append data to list of dictionaries with shares in users portfolio
    for i in range(l):
        symbol = row[i]["symbol"]
        s = lookup(symbol)
        name = s["name"]
        shares = row[i]["shares"]
        price = s["price"]
        total = shares * price

        # count saldo
        saldo = saldo + total

        # append 1 row in list
        tab.append({"symbol" : symbol, "name" : name, "shares" : shares, "price" : price, "total" : total})

    # get data from users table
    c = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    # round user saldo and cash
    cash = round(c[0]["cash"], 2)
    saldo = round(saldo + cash, 2)

    return render_template("layout.html", tab = tab, saldo = saldo, cash = cash)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        # empty form
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        if not request.form.get("shares"):
            return apology("must provide shares", 403)

        # fraction number of shares
        sh = float(request.form.get("shares"))
        if (sh - int(sh) != 0) :
            return apology("must provide integer number of shares", 403)

        # negative number of shares
        if sh < 1:
            return apology("must provide greater then 0 number of shares", 403)

        # get company symbol
        sym = request.form.get("symbol")
        s = lookup(sym)
        symbol = s["symbol"]

        # get data from user and stock table
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        s_rows = db.execute("SELECT * FROM stock WHERE owner_id = ? AND symbol = ?", session["user_id"], symbol)

        # check if user has enough money for transaction, get actual price
        total_price = sh * s["price"]
        cash = rows[0]["cash"]
        if total_price > cash:
            return apology("not enough money", 403)

        # add stock to user portfolio
        if len(s_rows) == 0:
            db.execute("INSERT INTO stock (owner_id, symbol, shares) VALUES (?,?,?)", session["user_id"], symbol, sh)
        else:
            ps = s_rows[0]["shares"]
            db.execute("UPDATE stock SET shares = ? WHERE owner_id = ? AND symbol = ?", sh + ps, session["user_id"], symbol)

        # change user cash in users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, session["user_id"])

        # set datatime
        now = datetime.datetime.now()
        now.strftime("%Y-%m-%d %X")

        # insert buy transaction into history table
        db.execute("INSERT INTO history (owner_id, symbol, shares, price, date) VALUES (?,?,?,?,?)", session["user_id"], symbol, sh, s["price"], now)

        return redirect("/")
    else:
        return render_template("buy.html")

#    """Buy shares of stock"""
#    return apology("TODO")


@app.route("/history")
@login_required
def history():

    rows = db.execute("SELECT * FROM history WHERE owner_id = ?", session["user_id"])
    l = len(rows)
    # list of dictionaries
    tab = []

    # append data to list of dictionaries, to tab
    for i in range(l):
        symbol = rows[i]["symbol"]
        shares = rows[i]["shares"]
        price = rows[i]["price"]
        date = rows[i]["date"]

        tab.append({"symbol" : symbol, "shares" : shares, "price" : price, "date" : date})

    # send data to proper html
    return render_template("history.html", tab = tab)
#    """Show history of transactions"""
#    return apology("TODO")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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

    if request.method == "POST":

        # empty form
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)

        # get company symbol
        symbol = request.form.get("symbol")
        s = lookup(symbol)

        # go to html and send proper data
        return render_template("quoted.html", name = s["name"], price = s["price"], symbol = s["symbol"])

    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # empty form
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)

        # check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                username=request.form.get("username"))

        if len(rows) != 0:
            return apology("username already exists", 403)

        # get data from form
        username=request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # is password equal to confirmation
        if password != confirmation:
            return apology("must provide password equal confirmation", 403)

        # hash password
        h = generate_password_hash(password)

        # add new user into users table
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", username, h)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    if request.method == "POST":

        symbol = request.form.get("symbol")
        total_price = 0

        # empty form
        if not request.form.get("shares"):
            return apology("must provide shares", 403)

        # number of shares to sell and owned shares
        s_shares = int(request.form.get("shares"))
        g = db.execute("SELECT shares FROM stock WHERE owner_id = ? AND symbol = ?", session["user_id"], symbol)
        g_shares = int(g[0]["shares"])

        # check if number of selling stocks is owned by user
        if (s_shares > g_shares):
            return apology("not have enough shares to sell", 403)

        # actual price and price of whole transaction
        price = lookup(symbol)["price"]
        total_price = s_shares * price

        # cash at users account
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]

        # sell stocks, change in stock table
        if (s_shares < g_shares):
            db.execute("UPDATE stock SET shares = ? WHERE owner_id = ? AND symbol = ?", g_shares - s_shares, session["user_id"], symbol)

        if (s_shares == g_shares):
            db.execute("DELETE FROM stock WHERE owner_id = ? AND symbol = ?", session["user_id"], symbol)

        # change cash in users table
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + total_price, session["user_id"])

        # set datatime
        now = datetime.datetime.now()
        now.strftime("%Y-%m-%d %X")

        # write sell transaction in history table
        db.execute("INSERT INTO history (owner_id, symbol, shares, price, date) VALUES (?,?,?,?,?)", session["user_id"], symbol, s_shares * (-1), price, now)

        return redirect("/")

    else:
        # list of symbols of owned companies
        symbols = []
        l = len(db.execute("SELECT symbol FROM stock WHERE owner_id = ?", session["user_id"]))

        # get symbols of companies from table and append to symbols list
        for i in range(l):
            row = db.execute("SELECT * FROM stock WHERE owner_id = ?", session["user_id"])
            s = row[i]["symbol"]
            symbol = lookup(s)["symbol"]
            symbols.append(symbol)

        return render_template("sell.html", symbols = symbols)

#    """Sell shares of stock"""
#    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

# change users password
# my personal touch
@app.route("/ch_pass", methods=["GET", "POST"])
@login_required
def ch_pass():

    if request.method == "POST":

        # for empty form
        if not request.form.get("password"):
            return apology("must provide password", 403)

        if not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)

        # get data from form
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # password equal confirmation
        if password != confirmation:
            return apology("must provide password equal confirmation", 403)

        row = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        old_password = row[0]["hash"]
        # hash new password
        h = generate_password_hash(password)

        # check if new password is new, compare with old
        if old_password == h:
            return apology("old password equal new password", 403)

        # change password in users table
        db.execute("UPDATE users SET hash = ? WHERE id = ?", h, session["user_id"])

        return redirect("/")

    else:
        return render_template("ch_pass.html")