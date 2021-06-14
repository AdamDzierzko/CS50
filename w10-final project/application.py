import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

#from helpers import apology, login_required, lookup, usd
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
#app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///magazyn.db")

#@app.route("/")
#def index():

#    return render_template("layout.html")


# @app.route("/user", methods=["GET", "POST"])
@app.route("/")
def user():

    rows = db.execute("SELECT * FROM user")
    print(rows)
    user_tab = []

    for i in range(len(rows)):
        id = rows[i]["id"]
        name = rows[i]["name"]
        date = rows[i]["date"]

        user_tab.append({"id" : id, "name" : name, "date" : date})

    return render_template("user.html", user_tab = user_tab)


@app.route("/addUser", methods=["POST"])
def addUser():

    u_name = request.form.get("u_name")

    # set datatime
    now = datetime.datetime.now()
    now.strftime("%Y-%m-%d %X")

    db.execute("INSERT INTO user (name, date) VALUES (?,?)", u_name, now)

    return redirect("/")

@app.route("/updateUser", methods=["POST"])
def updateUser():

    u_name = request.form.get("u_name")
    u_id = request.form.get("u_id")

    # set datatime
    now = datetime.datetime.now()
    now.strftime("%Y-%m-%d %X")

    db.execute("UPDATE user SET name = ?, date = ? WHERE id = ?", u_name, now, u_id)

    return redirect("/")

@app.route("/deleteUser", methods=["POST"])
def deleteUser():

    u_id = request.form.get("u_id")

    db.execute("DELETE FROM user WHERE id = ?", u_id)

    return redirect("/")



@app.route("/produkty")
def produkty():

    rows = db.execute("SELECT * FROM produkty")
    print(rows)
    produkty_tab = []

    for i in range(len(rows)):
        produkt_id = rows[i]["produkt_id"]
        numer = rows[i]["numer"]
        nazwa = rows[i]["nazwa"]
        date = rows[i]["date"]

        user_id = rows[i]["user_id"]
        u_n = db.execute("SELECT * FROM user WHERE id = ?", user_id)
        user_name = u_n[0]["name"]

        o_row = db.execute("SELECT * FROM opis_pr WHERE produkt_id = ?", produkt_id)
        print(o_row)
        opis_p = o_row[0]["opis"]

        produkty_tab.append({"produkt_id" : produkt_id, "numer" : numer, "nazwa" : nazwa, "date" : date, "user_name" : user_name, "opis_p" : opis_p})

    names = []
    row = db.execute("SELECT * FROM user")
    l = len(row)

    for i in range(l):
        name = row[i]["name"]
        names.append(name)

    return render_template("produkty.html", produkty_tab = produkty_tab, names = names)

@app.route("/addProdukty", methods=["POST"])
def addProdukty():

    u_name = request.form.get("name")
    numer = request.form.get("numer")
    nazwa = request.form.get("nazwa")
    opis = request.form.get("opis")

    id_row = db.execute("SELECT * FROM user WHERE name = ?", u_name)

    user_id = id_row[0]["id"]

    # set datatime
    now = datetime.datetime.now()
    now.strftime("%Y-%m-%d %X")

    db.execute("INSERT INTO produkty (numer, nazwa, user_id, date) VALUES (?,?,?,?)", numer, nazwa, user_id, now)

    p_row = db.execute("SELECT * FROM produkty WHERE nazwa = ?", nazwa)
    p_id = p_row[0]["produkt_id"]

    db.execute("INSERT INTO opis_pr (produkt_id, opis, user_id, date) VALUES (?,?,?,?)", p_id, opis, user_id, now)

    return redirect("/produkty")

@app.route("/updateProdukty", methods=["POST"])
def updateProdukty():

    u_name = request.form.get("name")
    numer = request.form.get("numer")
    nazwa = request.form.get("nazwa")
    p_id = request.form.get("p_id")
    opis = request.form.get("opis")

    id_row = db.execute("SELECT * FROM user WHERE name = ?", u_name)

    user_id = id_row[0]["id"]

    # set datatime
    now = datetime.datetime.now()
    now.strftime("%Y-%m-%d %X")

    db.execute("UPDATE produkty SET nazwa = ?, numer = ?, user_id = ?, date = ? WHERE produkt_id = ?", nazwa, numer, user_id, now, p_id)

    db.execute("UPDATE opis_pr SET opis = ?, user_id = ?, date = ? WHERE produkt_id = ?", opis, user_id, now, p_id)

    return redirect("/produkty")

@app.route("/deleteProdukty", methods=["POST"])
def deleteProdukty():

    p_id = request.form.get("p_id")

    db.execute("DELETE FROM opis_pr WHERE produkt_id = ?", p_id)

    db.execute("DELETE FROM produkty WHERE produkt_id = ?", p_id)

    return redirect("/produkty")

@app.route("/czesci")
def czesci():

    rows = db.execute("SELECT * FROM czesci")
    print(rows)
    czesci_tab = []


    for i in range(len(rows)):
        czesc_id = rows[i]["czesc_id"]
        nazwa = rows[i]["nazwa"]
        ilosc = rows[i]["ilosc"]
        typ = rows[i]["typ"]
        date = rows[i]["date"]

        user_id = rows[i]["user_id"]
        u_n = db.execute("SELECT * FROM user WHERE id = ?", user_id)
        user_name = u_n[0]["name"]

        o_row = db.execute("SELECT * FROM opis_cz WHERE czesc_id = ?", czesc_id)
        opis_cz = o_row[0]["opis"]

        czesci_tab.append({"czesc_id" : czesc_id, "nazwa" : nazwa, "ilosc" : ilosc, "typ" : typ, "user_name" : user_name, "date" : date, "opis_cz" : opis_cz})


    names = []
    row = db.execute("SELECT * FROM user")
    l = len(row)

    for i in range(l):
        name = row[i]["name"]
        names.append(name)

    return render_template("czesci.html", czesci_tab = czesci_tab, names = names)


@app.route("/addCzesci", methods= ["POST"])
def addCzesci():

    u_name = request.form.get("name")
    nazwa = request.form.get("nazwa")
    ilosc = request.form.get("ilosc")
    typ = request.form.get("typ")
    opis = request.form.get("opis")

    id_row = db.execute("SELECT * FROM user WHERE name = ?", u_name)

    user_id = id_row[0]["id"]

    # set datatime
    now = datetime.datetime.now()
    now.strftime("%Y-%m-%d %X")

    db.execute("INSERT INTO czesci (nazwa, ilosc, typ, user_id, date) VALUES (?,?,?,?,?)", nazwa, ilosc, typ, user_id, now)

    c_row = db.execute("SELECT * FROM czesci WHERE nazwa = ?", nazwa)
    c_id = c_row[0]["czesc_id"]

    db.execute("INSERT INTO opis_cz (czesc_id, opis, user_id, date) VALUES (?,?,?,?)", c_id, opis, user_id, now)

    return redirect("/czesci")

@app.route("/updateCzesci", methods=["POST"])
def updateCzesci():

    u_name = request.form.get("name")
    nazwa = request.form.get("nazwa")
    ilosc = request.form.get("ilosc")
    typ = request.form.get("typ")
    c_id = request.form.get("c_id")
    opis = request.form.get("opis")

    id_row = db.execute("SELECT * FROM user WHERE name = ?", u_name)

    user_id = id_row[0]["id"]

    # set datatime
    now = datetime.datetime.now()
    now.strftime("%Y-%m-%d %X")

    db.execute("UPDATE czesci SET nazwa = ?, ilosc = ?, typ = ?, user_id = ?, date = ? WHERE czesc_id = ?", nazwa, ilosc, typ, user_id, now, c_id)

    db.execute("UPDATE opis_cz SET opis = ?, user_id = ?, date = ? WHERE czesc_id = ?", opis, user_id, now, c_id)

    return redirect("/czesci")

@app.route("/deleteCzesci", methods=["POST"])
def deleteCzesci():

    c_id = request.form.get("c_id")

    db.execute("DELETE FROM opis_cz WHERE czesc_id = ?", c_id)

    db.execute("DELETE FROM czesci WHERE czesc_id = ?", c_id)

    return redirect("/czesci")