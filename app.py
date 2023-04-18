# import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
# from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def inbox():
    """Show all emails"""
    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE recipient = ?", username)

    return render_template("/index.html", emails=emails, username=username)


@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    """create email"""
    if request.method == "GET":
        userID = session["user_id"]
        senderDB = db.execute("SELECT username FROM users WHERE id = ?", userID)
        sender = senderDB[0]["username"]
        return render_template("compose.html", sender=sender)
    else:
        sender = request.form.get("sender")
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        body = request.form.get("body")

        if not sender or not recipient or not subject or not body:
            return apology("please fill in all fields")

        db.execute("INSERT into emails (sender, recipient, subject, body) VALUES (?, ?, ?, ?)", sender, recipient, subject, body)

        return redirect("/sent")

@app.route("/sent")
@login_required
def sent():
    """Show all sent emails"""
    userId = session["user_id"]
    usernameDB = db.execute("SELECT username FROM users WHERE id = ?", userId)
    username = usernameDB[0]["username"]
    emails = db.execute("SELECT * FROM emails WHERE sender = ?", username)

    return render_template("/index.html", emails=emails, username=username)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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


@app.route("/email", methods=["POST"])
@login_required
def email():
    """see email details."""
    if request.method == "POST":
        emailId = request.form.get("emailId")
        emailDetailDB = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
        emailDetail = emailDetailDB[0]
        return render_template("email.html", emailDetail=emailDetail)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
       #create variables from form fields on register.html
       email = request.form.get("email")
       password = request.form.get("password")
       confirm = request.form.get("confirm")

        #send error msg if any of the fields are empty
       if not email or not password or not confirm:
           return apology("please fill in all fields")

        #send error msg if password doesn't match what's in confirm field
       if password != confirm:
           return apology("passwords don't match")

        #using hashing function from helpers.py to hash password.
       hash = generate_password_hash(confirm)
        #try to add new user into users table
       try:
           newUser = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", email, hash)
        #if error, return apology
       except:
           return apology("This email already exists")
        #keep user logged in based on their id
       session["user_id"] = newUser

       return redirect("/")

@app.route("/reply", methods=["POST"])
@login_required
def reply():
    """reply to your email."""
    if request.method == "POST":
        emailId = request.form.get("emailId")
        emailDetailDB = db.execute("SELECT * FROM emails WHERE id = ?", emailId)
        emailDetail = emailDetailDB[0]
        return render_template("reply.html", emailDetail=emailDetail)

@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """ Change Password """

    # if method GET, display password change form
    if request.method == "GET":
        return render_template("password.html")

    # if method POST, change password
    else:
        # return apologies if form not filled out
        if not request.form.get("oldpass") or not request.form.get("newpass") or not request.form.get("confirm"):
            return apology("missing old or new password", 400)

        # save variables from form
        oldpass = request.form.get("oldpass")
        newpass = request.form.get("newpass")
        confirm = request.form.get("confirm")

        # user's previous password
        hash = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])
        hash = hash[0]['hash']

        # if old password incorrect, return apology
        if not check_password_hash(hash, oldpass):
            return apology("old password incorrect", 400)

        # if new passwords don't match, return apology
        if newpass != confirm:
            return apology("new passwords do not match", 400)

        # hash new password
        hash = generate_password_hash(confirm)

        # insert new hashed password into users table
        db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash=hash, id=session["user_id"])

        return redirect("/logout")
