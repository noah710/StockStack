from google.cloud import datastore
import json
import datetime
import hashlib
import os
import yfinance as yf


from flask import (
    Flask,
    Response,
    abort,
    render_template,
    request,
    jsonify,
    redirect,
    session,
    make_response
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

@app.route("/", methods=["GET", "POST"])
def search():
    return redirect("/results")

def get_default_ticker_info(ticker_symbol):

    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    asset_name = info.get('shortName', None)
    description = info.get('longBusinessSummary', None)
    country = info.get('country', None)

    if (isinstance(country, str) is not True):
        country = 'N/A'

    results = [ticker_symbol, asset_name, 'Country: ' + country, description]

    return results

def get_default_dates_and_prices(ticker_symbol):

    ticker = yf.Ticker(ticker_symbol)
    ticker_history = ticker.history(period = "1mo", interval = "1d")

    dates = []
    prices = []
    for d in range(len(ticker_history.index)):
        cur = str(ticker_history.index[d])
        dates.append(cur[0:10])

        price_rounded = round(ticker_history, 2)
        price_cur_date = str(price_rounded['Close'].iloc[d])
        prices.append(price_cur_date)

    data = {dates[i]: prices[i] for i in range(len(dates))}

    return data

@app.route("/results", methods=["GET", "POST"])
def loadResults():
    query = request.form.get("query")
    results = get_default_ticker_info(query)
    data = get_default_dates_and_prices(query)
    return render_template("results.html", query = results, data = json.dumps(data))

@app.route("/register", methods=["GET"])
def serve_register_form():

    return render_template("register.html")

@app.route("/register", methods=["GET", "POST"])
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
