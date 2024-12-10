import os
import datetime


from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = "sqlite:///database.db"


@app.route("/intro")
def intro():
    return render_template("/intro.html")

@app.route("/")
@login_required
def search():
    return render_template("index.html")

@app.route("/list")
@login_required
def list():
    id = session["user_id"]
    items = db.execute("SELECT * FROM list WHERE id = :id", id=id)
    return render_template("list.html", items=items)

@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    """ Add a list item """
    if request.method == "POST":
        item = request.form.get("item")
        add = db.execute("INSERT INTO list (id, item)  VALUES(:id, :item)", id=session["user_id"], item=item)
        return redirect("/list")
    else:
        return render_template("/add.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("/login.html", error = "You haven't entered username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("/login.html", error = "You haven't entered password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username AND hash = :hash", username=request.form.get("username"), hash=request.form.get("password"))
        if not rows:
            return render_template("login.html", error="Wrong username or password")

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


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        item = request.form.get("item")
        delete = db.execute("DELETE FROM list WHERE id = :id AND item = :item", id=session["user_id"], item=item)
        return redirect("/list")
    else:
        items = db.execute("SELECT * FROM list WHERE id = :id", id=session["user_id"])
        return render_template("/delete.html", items=items)

@app.route("/editlist", methods=["GET", "POST"])
@login_required
def editlist():
    if request.method == "POST":
        new = request.form.get("new")
        item = request.form.get("item")
        delete = db.execute("UPDATE list SET item = :new WHERE id = :id AND item = :item", new=new, id=session["user_id"], item=item)
        return redirect("/list")
    else:
        items = db.execute("SELECT * FROM list WHERE id = :id", id=session["user_id"])
        return render_template("/editlist.html", items=items)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("/register.html", error = "You haven't entered a username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("/register.html", error = "You haven't entered a password")

        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("/register.html", error = "The passwords aren't the same")
        # Gets first row in reversed query then takes the list that is returned and gets the first element then the value in the key 'id' and pluses one.
        test = db.execute("SELECT * FROM users")
        if not test:
            new_id = 1
        else:
            new_id = db.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")[0]['id']+1

        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users (id, username, hash, email, name, pic)  VALUES(:id, :username, :hash, :email, :name, :pic)", id=new_id, username=request.form.get("username"), hash=request.form.get("password"), email=request.form.get("email"), name=request.form.get("name"), pic='http://dragene.no/wp-content/uploads/2016/06/default1.jpg')
        if not result:
            return render_template("/register.html", error = "Error 403. Please report this to the owner of this website immediately!")
        result = db.execute("INSERT INTO new (id, new)  VALUES(:id, :new)", id=new_id, new=0)
        session["user_id"] = new_id
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/settings", methods=["GET"])
@login_required
def settings():
    name = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])[0]['username']
    word = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])[0]['hash']
    title = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])[0]['hash']
    pic = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])[0]['pic']
    return render_template("settings.html", name=name, word=word, pic=pic)

@app.route("/name", methods=["POST"])
@login_required
def name():
    name = request.form.get("username")
    result = db.execute("UPDATE users SET username = :name WHERE id = :id", name=name,id=session["user_id"])
    return redirect("/settings")

@app.route("/password", methods=["POST"])
@login_required
def password():
    old = request.form.get("old")
    new = request.form.get("new")
    result = db.execute("UPDATE users SET hash = :new WHERE id = :id", new=new,id=session["user_id"])
    return redirect("/settings")

@app.route("/delacc", methods=["POST"])
@login_required
def delacc():
    delete1 = db.execute("DELETE FROM list WHERE id = :id", id=session["user_id"])
    delete2 = db.execute("DELETE FROM mail WHERE by = :id OR too = :id", id=session["user_id"])
    delete3 = db.execute("DELETE FROM users WHERE id = :id", id=session["user_id"])
    delete4 = db.execute("DELETE FROM texts WHERE id = :id", id=session["user_id"])
    delete5 = db.execute("DELETE FROM new WHERE id = :id", id=session["user_id"])
    session.clear()
    return redirect("/")

@app.route("/mail", methods=["GET", "POST"])
@login_required
def mail():
    if request.method == "GET":
        new = db.execute("UPDATE new SET new = :new WHERE id = :id", new=0,id=session["user_id"])
        mail = db.execute("SELECT * FROM mail WHERE by = :id OR too = :id", id=session["user_id"])
        users = db.execute("SELECT * FROM users WHERE NOT id = :id ", id=session["user_id"])
        for i in mail:
            newby = db.execute("SELECT username FROM users WHERE id = :id", id=i['by'])[0]['username']
            i['by']=newby
            newtoo = db.execute("SELECT username FROM users WHERE id = :id", id=i['too'])[0]['username']
            i['too']=newtoo
        return render_template("/mail.html", mail=mail, users=users)
    else:
        result = db.execute("INSERT INTO mail (title, mail, by, too)  VALUES(:title, :mail, :by, :too)", title=request.form.get("title"), mail=request.form.get("mail"), by=session["user_id"], too=request.form.get("to"))
        new = db.execute("UPDATE new SET new = new + 1 WHERE id = :too", too=request.form.get("to"))
        return redirect("/mail")

@app.route("/view", methods=["GET"])
@login_required
def view():
    mails = db.execute("SELECT * FROM mail WHERE by = :id OR too = :id", id=session["user_id"])
    return render_template("/view.html", mails=mails)

@app.route("/edit", methods=["POST"])
@login_required
def edit():
    if request.form.get("title1"):
        title = request.form.get("title1")
        print(title)
        mailfrom = db.execute("SELECT by FROM mail WHERE title = :title", title=title)[0]['by']
        mail = db.execute("SELECT mail FROM mail WHERE title = :title", title=title)[0]['mail']
        if mailfrom == session["user_id"]:
            own = True
            return render_template("edit.html", title = title, mail=mail,own=own)
        else:
            return render_template("edit.html", title = title, mail=mail)
    else:
        new = request.form.get("new")
        title = request.form.get("title")
        result = db.execute("UPDATE mail SET mail = :new WHERE title = :title", new=new,title=title)
        return redirect("/mail")

@app.route("/text", methods=["GET", "POST"])
@login_required
def text():
    if request.method == "POST":
        now = datetime.datetime.now()
        date = now.strftime('%Y-%m-%d %H:%M:%S')
        result = db.execute("INSERT INTO texts (id, title, text_message, date)  VALUES(:id, :title, :text_message, :date)", id=session["user_id"], title=request.form.get("title"), text_message=request.form.get("text_message"), date=date)
        return redirect("/text")
    else:
        texts = db.execute("SELECT * FROM texts WHERE id = :id", id=session["user_id"])
        return render_template("/text.html", texts=texts)

@app.route("/textview", methods=["GET"])
@login_required
def textview():
    texts = db.execute("SELECT * FROM texts WHERE id = :id", id=session["user_id"])
    return render_template("/textview.html", texts=texts)

@app.route("/textedit", methods=["POST"])
@login_required
def textedit():
    if request.form.get("new"):
        new = request.form.get("new")
        result = db.execute("UPDATE texts SET text_message = :new WHERE id = :id", new=new,id=session["user_id"])
        return redirect("/text")
    else:
        title = request.form.get("title")
        text = db.execute("SELECT * FROM texts WHERE title = :title AND id = :id", title=title, id=session["user_id"])[0]['text_message']
        return render_template("/textedit.html", title = title, text=text)

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "GET":
        users = db.execute("SELECT * FROM users")
        return render_template("/forgot.html", users=users)
    else:
        new = request.form.get("new")
        result = db.execute("UPDATE users SET hash = :new WHERE id = :id", new=new,id=request.form.get("name"))
        return render_template("login.html", error="Your password has been updated")

@app.route("/pfp", methods=["POST"])
@login_required
def pfp():
    if request.form.get("new") != "Default":
        result = db.execute("UPDATE users SET pic = :new WHERE id = :id", new=request.form.get("new"),id=session["user_id"])
    else:
        result = db.execute("UPDATE users SET pic = :new WHERE id = :id", new='http://dragene.no/wp-content/uploads/2016/06/default1.jpg', id=session["user_id"])
    return redirect("/settings")

@app.route("/calc", methods=["GET"])
@login_required
def calc():
    return render_template("/calc.html")

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    text = len(db.execute("SELECT * FROM texts WHERE id = :id", id=session["user_id"]))
    mail = len(db.execute("SELECT * FROM mail WHERE by = :id OR too = :id", id=session["user_id"]))
    lists = len(db.execute("SELECT * FROM list WHERE id = :id", id=session["user_id"]))
    new = db.execute("SELECT new FROM new WHERE id = :id",id=session["user_id"])[0]['new']
    name = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])[0]['username']
    pic = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])[0]['pic']
    user = len(db.execute("SELECT * FROM users"))
    users = db.execute("SELECT * FROM users WHERE NOT username = :name", name='Owner')
    if name == "Owner":
        mod = True
        return render_template("profile.html", name=name, text=text, lists=lists, mail=mail, new=new, mod=mod, users=users, user=user,pic=pic)
    return render_template("profile.html", name=name, text=text, lists=lists, mail=mail, new=new, users=users, user=user, pic=pic)

@app.route("/tictactoe", methods=["GET"])
@login_required
def tictactoe():
    return render_template("tictactoe.html")

@app.route("/paint", methods=["GET"])
@login_required
def paint():
    return render_template("paint.html")

@app.route("/snake", methods=["GET"])
@login_required
def snake():
    return render_template("snake.html")

@app.route("/encipher", methods=["GET"])
@login_required
def encipher():
    s = request.form.get("key")
    text = request.form.get("text")
    print(encipher(text,s))
    return render_template("encipher.html")

@app.route("/news", methods=["GET"])
@login_required
def news():
    return render_template("news.html")


