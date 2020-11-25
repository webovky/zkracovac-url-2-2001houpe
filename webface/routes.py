from . import app
from flask import render_template, request, redirect, url_for, session, flash
import functools
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Shortener
from pony.orm import db_session
import string
import random

# from werkzeug.security import check_password_hash


def login_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    shortcut = "".join([random.choice(string.ascii_letters) for i in range(7)])
    print(shortcut)

    if "user" in sessin:
        user = User.get(login=session["user"])
        for addr in user.addresses:
            print(addr.shortcut, addr.url)

    return render_template("base.html.j2")


@app.route("/<string:shortcut>", methods=["GET"])
def short_redirect(shortcut):
    shortener = Shortener.get(shortcut=shortcut)
    if shortener.user:
        print(shortener.user.login)
    return render_template("base.html.j2")


@app.route("/adduser/", methods=["GET"])
def adduser():
    return render_template("adduser.html.j2")


@app.route("/adduser/", methods=["POST"])
@db_session
def adduser_post():
    login = None
    passwd1 = None
    passwd2 = None
    user = User.get(email="nozka@spseol.cz")
    user = User[login]  # do [] jen primární klíč
    if user:
        flash("Uživatel již existuje. Zvolte si jiné uživatelské jméno.")
        print(user.login, user.password)
    if len(passwd1) >= 5 and passwd1 == passwd2:
        user = User(login=login, password=generate_password_hash(passwd1))
        flash("účet vytvořen")
    else:
        flash("hesla nejsou stejná, nebo jsou příliš krátká")
        return redirect(url_for("adduser"))
    return redirect(url_for("index"))


@app.route("/login/")
def login():
    return render_template("login.html.j2")


@app.route("/login/", methods=["POST"])
def login_post():
    login = None
    passwd = None
    user = User[login]
    if user and check_password_hash(user.password, passwd):
        session["user"] = login
        flash("Uspěšně jsi se přihlásil!")
    else:
        flash("Nezprávné přihlašovací údaje!")
    return redirect(url_for("index"))


@app.route("/logout/")
def logout():
    session.pop("user", None)
    flash("Odhlášeno")
    return render_template("base.html.j2")
