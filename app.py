# Import standard Python libraries for operating system interactions and date/time handling
import os
import datetime

# Import Flask and related modules for building the web application
from flask import Flask, flash, jsonify, redirect, render_template, request, session
# Import Flask-Session for server-side session management
from flask_session import Session
# Import tempfile for creating temporary directories for session storage
from tempfile import mkdtemp
# Import Werkzeug utilities for exception handling and password security
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Import CS50's SQL module for database interaction
from cs50 import SQL

# Import custom helper functions, including a login requirement decorator
from helpers import login_required

# --- Application Initialization and Configuration ---

# Create a Flask application instance with the current module name
app = Flask(__name__)

# Enable automatic reloading of templates during development for instant updates
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Define a function to prevent caching of responses after each request
@app.after_request
def after_request(response):
    """Ensure responses aren't cached to deliver fresh content to users"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0  # Set expiration to the past
    response.headers["Pragma"] = "no-cache"  # For compatibility with older browsers
    return response

# Configure session to use the filesystem instead of signed cookies for enhanced security
app.config["SESSION_FILE_DIR"] = mkdtemp()  # Create a temporary directory for session files
app.config["SESSION_PERMANENT"] = False  # Sessions are not permanent; they expire when the browser closes
app.config["SESSION_TYPE"] = "filesystem"  # Use filesystem-based session storage
Session(app)  # Initialize the session extension with the app

# Initialize the SQLite database connection using cs50.SQL
# This assumes a file named 'database.db' exists in the same directory as app.py
db = SQL("sqlite:///database.db")

# --- Route Definitions ---

@app.route("/intro")
def intro():
    """Render the introductory page of the application"""
    return render_template("/intro.html")

@app.route("/")
@login_required
def search():
    """Render the main authenticated homepage"""
    return render_template("index.html")

@app.route("/list")
@login_required
def list():
    """Display the user's list items"""
    user_id = session["user_id"]
    items = db.execute("SELECT * FROM list WHERE id = :id", id=user_id)
    return render_template("list.html", items=items)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Handle adding a new item to the user's list"""
    if request.method == "POST":
        item = request.form.get("item")
        db.execute("INSERT INTO list (id, item) VALUES(:id, :item)", id=session["user_id"], item=item)
        return redirect("/list")
    else:
        return render_template("/add.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login functionality"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("/login.html", error="You haven't entered username")
        if not password:
            return render_template("/login.html", error="You haven't entered password")

        # Use hashed passwords for security (assuming 'hash' column stores hashed passwords)
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if not rows or not check_password_hash(rows[0]["hash"], password):
            return render_template("login.html", error="Wrong username or password")

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log the user out and redirect to the homepage"""
    session.clear()
    return redirect("/")

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Handle deletion of list items"""
    if request.method == "POST":
        item = request.form.get("item")
        db.execute("DELETE FROM list WHERE id = :id AND item = :item", id=session["user_id"], item=item)
        return redirect("/list")
    else:
        items = db.execute("SELECT * FROM list WHERE id = :id", id=session["user_id"])
        return render_template("/delete.html", items=items)

@app.route("/editlist", methods=["GET", "POST"])
@login_required
def editlist():
    """Handle editing of existing list items"""
    if request.method == "POST":
        new_item = request.form.get("new")
        old_item = request.form.get("item")
        db.execute("UPDATE list SET item = :new WHERE id = :id AND item = :item", 
                   new=new_item, id=session["user_id"], item=old_item)
        return redirect("/list")
    else:
        items = db.execute("SELECT * FROM list WHERE id = :id", id=session["user_id"])
        return render_template("/editlist.html", items=items)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle new user registration"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return render_template("/register.html", error="You haven't entered a username")
        if not password:
            return render_template("/register.html", error="You haven't entered a password")
        if password != confirmation:
            return render_template("/register.html", error="The passwords aren't the same")

        # Check if username already exists
        if db.execute("SELECT * FROM users WHERE username = :username", username=username):
            return render_template("/register.html", error="Username already exists")

        # Get the next available ID (though SQLite can auto-increment this if set up properly)
        test = db.execute("SELECT * FROM users")
        if not test:
            new_id = 1
        else:
            new_id = db.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1")[0]['id'] + 1

        # Hash the password for secure storage
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        result = db.execute(
            "INSERT INTO users (id, username, hash, email, name, pic) VALUES(:id, :username, :hash, :email, :name, :pic)",
            id=new_id, 
            username=username, 
            hash=hashed_password,
            email=request.form.get("email"), 
            name=request.form.get("name"), 
            pic='http://dragene.no/wp-content/uploads/2016/06/default1.jpg'
        )

        if not result:
            return render_template("/register.html", error="Error 403. Please report this to the owner of this website immediately!")
        
        db.execute("INSERT INTO new (id, new) VALUES(:id, :new)", id=new_id, new=0)
        session["user_id"] = new_id
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/settings", methods=["GET"])
@login_required
def settings():
    """Display the user's settings page"""
    user_id = session["user_id"]
    # Retrieve user details from the database
    user_data = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)[0]
    name = user_data['username']
    pic = user_data['pic']
    # Render settings page with user information
    return render_template("settings.html", name=name, word=word, pic=pic)

@app.route("/name", methods=["POST"])
@login_required
def name():
    """Update the user's username"""
    new_name = request.form.get("username")
    # Update the username in the database for the current user
    db.execute("UPDATE users SET username = :name WHERE id = :id", 
               name=new_name, id=session["user_id"])
    # Redirect back to settings
    return redirect("/settings")

@app.route("/password", methods=["POST"])
@login_required
def password():
    """Update the user's password after verifying the old password"""
    # Get the old and new passwords from the form
    old_password = request.form.get("old")
    new_password = request.form.get("new")

    # Ensure both old and new passwords are provided
    if not old_password:
        return render_template("settings.html", error="Please enter your current password")
    if not new_password:
        return render_template("settings.html", error="Please enter a new password")

    # Retrieve the current user's hashed password from the database
    user_id = session["user_id"]
    current_hash = db.execute("SELECT hash FROM users WHERE id = :id", id=user_id)[0]["hash"]

    # Verify the old password matches the stored hash
    if not check_password_hash(current_hash, old_password):
        return render_template("settings.html", error="Current password is incorrect")

    # Hash the new password for secure storage
    new_hash = generate_password_hash(new_password)

    # Update the password in the database with the new hash
    db.execute("UPDATE users SET hash = :new WHERE id = :id", new=new_hash, id=user_id)

    # Redirect back to settings with a success message (optional)
    return redirect("/settings")

@app.route("/delacc", methods=["POST"])
@login_required
def delacc():
    """Delete the user's account and all associated data"""
    user_id = session["user_id"]
    # Delete all related data from various tables
    db.execute("DELETE FROM list WHERE id = :id", id=user_id)  # List items
    db.execute("DELETE FROM mail WHERE by = :id OR too = :id", id=user_id)  # Mail
    db.execute("DELETE FROM users WHERE id = :id", id=user_id)  # User account
    db.execute("DELETE FROM texts WHERE id = :id", id=user_id)  # Texts
    db.execute("DELETE FROM new WHERE id = :id", id=user_id)  # Notification counters
    # Clear the session to log the user out
    session.clear()
    # Redirect to the homepage
    return redirect("/")

@app.route("/mail", methods=["GET", "POST"])
@login_required
def mail():
    """Handle mail viewing and sending"""
    user_id = session["user_id"]
    if request.method == "GET":
        # Reset the 'new' notification counter for this user
        db.execute("UPDATE new SET new = :new WHERE id = :id", new=0, id=user_id)
        # Retrieve all mails sent by or to this user
        mail = db.execute("SELECT * FROM mail WHERE by = :id OR too = :id", id=user_id)
        # Get a list of all other users for sending mail
        users = db.execute("SELECT * FROM users WHERE NOT id = :id", id=user_id)
        # Replace user IDs with usernames in mail data for display
        for i in mail:
            i['by'] = db.execute("SELECT username FROM users WHERE id = :id", id=i['by'])[0]['username']
            i['too'] = db.execute("SELECT username FROM users WHERE id = :id", id=i['too'])[0]['username']
        # Render the mail page with mail and user data
        return render_template("/mail.html", mail=mail, users=users)
    else:
        # Handle sending a new mail
        db.execute("INSERT INTO mail (title, mail, by, too) VALUES(:title, :mail, :by, :too)",
                   title=request.form.get("title"), 
                   mail=request.form.get("mail"), 
                   by=user_id, 
                   too=request.form.get("to"))
        # Increment the recipient's 'new' counter for notifications
        db.execute("UPDATE new SET new = new + 1 WHERE id = :too", too=request.form.get("to"))
        # Redirect back to the mail page
        return redirect("/mail")

@app.route("/view", methods=["GET"])
@login_required
def view():
    """Display all mails for the user (alternative view)"""
    # Retrieve all mails sent by or to the current user
    mails = db.execute("SELECT * FROM mail WHERE by = :id OR too = :id", id=session["user_id"])
    # Render a view page with the mails
    return render_template("/view.html", mails=mails)

@app.route("/edit", methods=["POST"])
@login_required
def edit():
    """Handle editing of mail content"""
    if request.form.get("title1"):
        # Handle request to edit a specific mail based on title
        title = request.form.get("title1")
        # Retrieve sender and content of the mail
        mailfrom = db.execute("SELECT by FROM mail WHERE title = :title", title=title)[0]['by']
        mail = db.execute("SELECT mail FROM mail WHERE title = :title", title=title)[0]['mail']
        # Check if the current user is the sender
        own = (mailfrom == session["user_id"])
        # Render edit page, indicating ownership if applicable
        return render_template("edit.html", title=title, mail=mail, own=own) if own else render_template("edit.html", title=title, mail=mail)
    else:
        # Handle submission of edited mail content
        new_content = request.form.get("new")
        title = request.form.get("title")
        # Update the mail content in the database
        # Note: Using title as identifier may affect multiple mails if titles are not unique
        db.execute("UPDATE mail SET mail = :new WHERE title = :title", new=new_content, title=title)
        # Redirect back to the mail page
        return redirect("/mail")

@app.route("/text", methods=["GET", "POST"])
@login_required
def text():
    """Handle creation and display of user texts"""
    if request.method == "POST":
        # Handle submission of a new text
        now = datetime.datetime.now()  # Get current timestamp
        date = now.strftime('%Y-%m-%d %H:%M:%S')  # Format as string
        # Insert the new text into the database
        db.execute("INSERT INTO texts (id, title, text_message, date) VALUES(:id, :title, :text_message, :date)",
                   id=session["user_id"], 
                   title=request.form.get("title"), 
                   text_message=request.form.get("text_message"), 
                   date=date)
        # Redirect back to the text page
        return redirect("/text")
    else:
        # Handle GET request by showing all texts for the user
        texts = db.execute("SELECT * FROM texts WHERE id = :id", id=session["user_id"])
        return render_template("/text.html", texts=texts)

@app.route("/textview", methods=["GET"])
@login_required
def textview():
    """Display all texts for the user (alternative view)"""
    # Retrieve all texts for the current user
    texts = db.execute("SELECT * FROM texts WHERE id = :id", id=session["user_id"])
    # Render a text view page
    return render_template("/textview.html", texts=texts)

@app.route("/textedit", methods=["POST"])
@login_required
def textedit():
    """Handle editing of text messages"""
    if request.form.get("new"):
        # Handle submission of edited text
        new_text = request.form.get("new")
        # Update all texts for the user (likely a bug; should target a specific text)
        db.execute("UPDATE texts SET text_message = :new WHERE id = :id", 
                   new=new_text, id=session["user_id"])
        # Redirect back to the text page
        return redirect("/text")
    else:
        # Handle request to edit a specific text based on title
        title = request.form.get("title")
        text = db.execute("SELECT * FROM texts WHERE title = :title AND id = :id", 
                          title=title, id=session["user_id"])[0]['text_message']
        # Render the text edit page
        return render_template("/textedit.html", title=title, text=text)

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    """Handle password reset (insecure implementation)"""
    if request.method == "GET":
        # Show a page listing all users for password reset selection
        users = db.execute("SELECT * FROM users")
        return render_template("/forgot.html", users=users)
    else:
        # Handle password reset submission
        new_password = request.form.get("new")
        user_id = request.form.get("name")  # Should be 'id', not 'name'
        # Update the user's password without verification (highly insecure)
        db.execute("UPDATE users SET hash = :new WHERE id = :id", new=new_password, id=user_id)
        # Redirect to login with a success message
        return render_template("login.html", error="Your password has been updated")

@app.route("/pfp", methods=["POST"])
@login_required
def pfp():
    """Update the user's profile picture"""
    new_pic = request.form.get("new")
    if new_pic != "Default":
        # Update with a custom profile picture URL
        db.execute("UPDATE users SET pic = :new WHERE id = :id", 
                   new=new_pic, id=session["user_id"])
    else:
        # Revert to the default profile picture
        db.execute("UPDATE users SET pic = :new WHERE id = :id", 
                   new='static/default.jpg', id=session["user_id"])
    # Redirect back to settings
    return redirect("/settings")

@app.route("/calc", methods=["GET"])
@login_required
def calc():
    """Render a calculator page"""
    # Render a calculator template, likely with client-side JavaScript
    return render_template("/calc.html")

@app.route("/profile", methods=["GET"])
@login_required
def profile():
    """Display the user's profile with statistics"""
    user_id = session["user_id"]
    # Calculate counts of various user data
    text_count = len(db.execute("SELECT * FROM texts WHERE id = :id", id=user_id))
    mail_count = len(db.execute("SELECT * FROM mail WHERE by = :id OR too = :id", id=user_id))
    list_count = len(db.execute("SELECT * FROM list WHERE id = :id", id=user_id))
    new_count = db.execute("SELECT new FROM new WHERE id = :id", id=user_id)[0]['new']
    name = db.execute("SELECT username FROM users WHERE id = :id", id=user_id)[0]['username']
    pic = db.execute("SELECT * FROM users WHERE id = :id", id=user_id)[0]['pic']
    total_users = len(db.execute("SELECT * FROM users"))
    other_users = db.execute("SELECT * FROM users WHERE NOT username = :name", name='Owner')
    
    # Check if the user is the 'Owner' for moderator status
    if name == "Owner":
        return render_template("profile.html", name=name, text=text_count, lists=list_count, 
                              mail=mail_count, new=new_count, mod=True, users=other_users, 
                              user=total_users, pic=pic)
    # Render profile for non-owner users
    return render_template("profile.html", name=name, text=text_count, lists=list_count, 
                          mail=mail_count, new=new_count, users=other_users, user=total_users, pic=pic)

@app.route("/tictactoe", methods=["GET"])
@login_required
def tictactoe():
    """Render a tic-tac-toe game page"""
    return render_template("tictactoe.html")

@app.route("/paint", methods=["GET"])
@login_required
def paint():
    """Render a painting application page"""
    return render_template("paint.html")

@app.route("/snake", methods=["GET"])
@login_required
def snake():
    """Render a snake game page"""
    return render_template("snake.html")

@app.route("/encipher", methods=["GET"])
@login_required
def encipher():
    """Render an enciphering tool page (incomplete implementation)"""
    # Note: This seems intended to process POST data but is defined as GET
    key = request.form.get("key")  # Should be moved to a POST method
    text = request.form.get("text")
    # 'encipher' function is undefined; this line would raise an error
    print(encipher(text, key))  # Placeholder for encryption logic
    return render_template("encipher.html")

@app.route("/news", methods=["GET"])
@login_required
def news():
    """Render a news page"""
    return render_template("ne ws.html")

# Note: The application assumes a database schema with tables: users, list, mail, texts, new
# Example schema (simplified):
# - users: id (int), username (text), hash (text), email (text), name (text), pic (text)
# - list: id (int), item (text)
# - mail: title (text), mail (text), by (int), too (int)
# - texts: id (int), title (text), text_message (text), date (text)
# - new: id (int), new (int)