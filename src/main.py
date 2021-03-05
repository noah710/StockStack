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
    return render_template("index.html")

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

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True) 
