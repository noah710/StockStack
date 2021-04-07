from flask import (
    Flask,
    Response,
    abort,
    render_template,
    request,
    jsonify,
    redirect,
    session,
    make_response,
    Blueprint
)

import json
import hashlib
import os
from google.cloud import datastore

blueprint = Blueprint('auth', __name__)

ds_client = datastore.Client()

@blueprint.route("/register", methods=["GET"])
def serve_register_form():

    return render_template("register.html")

@blueprint.route("/register", methods=["POST"])
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

@blueprint.route("/login", methods=["GET"])
def serve_login():
    return render_template("login.html")

@blueprint.route("/login", methods=["POST"])
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

@blueprint.route("/logout", methods=['POST'])
def handle_logout():
    # remove current user's session
    session.clear()
    # redirect to the home page 
    return redirect("/")


# helpers
def hash_password(password, salt):
    """This will give us a hashed password that will be extremlely difficult to
    reverse.  Creating this as a separate function allows us to perform this
    operation consistently every time we use it."""
    encoded = password.encode("utf-8")
    return hashlib.pbkdf2_hmac("sha256", encoded, salt, 100000)
