from google.cloud import datastore
import json
import datetime
import hashlib
import os


from flask import (
    Flask,
    Response,
    abort,
    render_template,
    request,
    jsonify,
    redirect,
    session,
)

ds_client = datastore.Client()

app = Flask(__name__)
app.secret_key = os.urandom(12)

def hash_password(password, salt):
    """This will give us a hashed password that will be extremlely difficult to
    reverse.  Creating this as a separate function allows us to perform this
    operation consistently every time we use it."""
    encoded = password.encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", encoded, salt, 100000)

@app.route("/")
def home():
    """Return a simple HTML page."""
    print("Hit the route!")

    # check if there is an active session
    user = session.get("user", None)

    # add user variable to homepage
    return render_template("index.html", user = user)

@app.route("/", methods=["POST"])
def search():
    return redirect("/results")

@app.route("/results")
def loadResults():
    query = request.form.get("query")
    return render_template("results.html", query = query)

@app.route("/register", methods=["GET"])
def serve_register_form():

    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    # get user input
    username = request.form.get("username")
    password = request.form.get("password")

    # TODO: check if user exist in database

    # generate password hash to store
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("utf-8")
    password_hash = hash_password(password, salt)

    # store user in db
    user_key = ds_client.key("UserCredential", username)
    user = datastore.Entity(key=user_key)
    user["username"] = username
    user["password_hash"] = password_hash
    user["salt"] = salt
    ds_client.put(user)

    session["user"] = username
    return redirect("/")
    # return render_template("index.html")

@app.route("/login", methods=["GET"])
def serve_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def handle_login():
    # get user input
    username = request.form.get("username")
    password = request.form.get("password")

    # check db if user exist
    user_key = ds_client.key("UserCredential", username)
    user = ds_client.get(user_key)
    if not user:
        return "User not found"

    # if it got here, that username is in our db
    pw_salt = user["salt"]
    pw_hash = hash_password(password, pw_salt)

    # check if hashes match
    if pw_hash != user["password_hash"]:
        return "Password invalid"

    # make new session and redirect to home page
    session["user"] = username
    return redirect("/")

@app.route("/aboutus", methods=["GET"])
def about_us():

	user = session.get("user", None)

	return render_template("aboutus.html", user = user)

@app.route("/profile", methods=["GET"])
def profile():

	#load the user from the session. You can only access the profile page after logging in, so this should always load.
	user = session.get("user", None)

	return render_template("profile.html", user = user)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
