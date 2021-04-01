from google.cloud import datastore
import json
import datetime
import hashlib
import os
import yfinance as yf
from yahoo_fin import stock_info as si

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
    
    #disgustingly hard-coded price-getter for curator's picks
    msft_ticker = yf.Ticker("msft")
    datas = msft_ticker.history()
    last_quote1 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before1 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    tsla_ticker = yf.Ticker("tsla")
    datas = tsla_ticker.history()
    last_quote2 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before2 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    aapl_ticker = yf.Ticker("aapl")
    datas = aapl_ticker.history()
    last_quote3 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before3 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    ge_ticker = yf.Ticker("ge")
    datas = ge_ticker.history()
    last_quote4 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before4 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    amzn_ticker = yf.Ticker("amzn")
    datas = amzn_ticker.history()
    last_quote5 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before5 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    nvda_ticker = yf.Ticker("nvda")
    datas = nvda_ticker.history()
    last_quote6 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before6 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    fb_ticker = yf.Ticker("fb")
    datas = fb_ticker.history()
    last_quote7 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before7 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    amd_ticker = yf.Ticker("amd")
    datas = amd_ticker.history()
    last_quote8 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before8 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    nflx_ticker = yf.Ticker("nflx")
    datas = nflx_ticker.history()
    last_quote9 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before9 = round((datas.tail(2)['Close'].iloc[0]), 2)
    
    twtr_ticker = yf.Ticker("twtr")
    datas = twtr_ticker.history()
    last_quote10 = round((datas.tail(1)['Close'].iloc[0]), 2)
    before10 = round((datas.tail(2)['Close'].iloc[0]), 2)

    
    # add user variable to homepage
    return render_template("index.html", user = user, price1 = last_quote1, price2 = last_quote2, price3 = last_quote3, price4 = last_quote4, price5 = last_quote5, price6 = last_quote6, price7 = last_quote7, price8 = last_quote8, price9 = last_quote9, price10 = last_quote10,
    price1b = before1, price2b = before2, price3b = before3, price4b = before4, price5b = before5, price6b = before6, price7b = before7, price8b = before8, price9b = before9, price10b = before10)

class UserTickerData:
    def __init__(self, symbol, buy_price, amount, date):
        self.symbol = symbol
        self.buy_price = buy_price
        self.amount = amount
        self.date = date

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

# Function returns portfolio base price (price paid for all assets), portfolio current price, and overall percentage gain/loss
def calculate_net_worth_data(ticker_list):

    return_list = []

    tickers = {}
    base_worth = 0

    # First calculate the portfolio base price
    for t in ticker_list:
        tickers[t.symbol] = t.amount

        # Calculate portfolio base worth 
        base_worth = base_worth + (t.buy_price * t.amount)

    cur_worth = 0

    for k, v in tickers.items():
        ticker = yf.Ticker(k)
        todays_data = ticker.history(period='1d')
        cur_worth = cur_worth + (todays_data['Close'][0] * v)

    base_rounded = round(base_worth, 2)
    cur_rounded = round(cur_worth, 2)

    percent_change = round((cur_rounded / base_rounded * 100 - 100), 3)

    base_final = format(base_rounded, '.2f')
    cur_final = format(cur_rounded, '.2f')

    return_list.append(base_final)
    return_list.append(cur_final)
    return_list.append(percent_change)
    return return_list

def get_top_gainers():
    top_gainers = si.get_day_gainers()
    
    for x in range(10):
        print(str(x + 1) + '.\n' + str(top_gainers['Symbol'][x]) + '\nName: ' + str(top_gainers['Name'][x]) + '\nPrice (Intraday): $' + 
        str(top_gainers['Price (Intraday)'][x]) + '\nChange ($): +$' + str(top_gainers['Change'][x]) + '\nPercent Change: +' + str(top_gainers["% Change"][x]) + "%\n")

@app.route("/results", methods=["POST"])
def loadResults():

	 # check if there is an active session
    user = session.get("user", None)

    query = request.form.get("query")
    results = get_default_ticker_info(query)
    data = get_default_dates_and_prices(query)
    return render_template("results.html", query = results, data = json.dumps(data), user = user)

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

@app.route("/logout", methods=['POST'])
def handle_logout():
    # remove current user's session
    session.clear();
    # redirect to the login page 
    return redirect("/login");

@app.route("/aboutus", methods=["GET"])
def about_us():

	user = session.get("user", None)

	return render_template("aboutus.html", user = user)

@app.route("/profile", methods=["GET"])
def profile():

	#load the user from the session. You can only access the profile page after logging in, so this should always load.
	user = session.get("user", None)

	return render_template("profile.html", user = user)

@app.route("/profile/add", methods=["POST"])
def add_to_portfolio():
    user = session.get("user", None)
    portfolio_key = ds_client.key("Portfolio", user)

    ticker = request.form.get("ticker")
    price = request.form.get("price")
    amount = request.form.get("amount")
    date = request.form.get("date")

    #user_entry = {'ticker':ticker, 'price':price, 'amount':amount, 'date':date}


    # check if the user has a portfolio    
    user_portfolio = ds_client.get(portfolio_key)
    #if this user has no portfolio, make a new one for user and update
    if user_portfolio is None:
        user_portfolio = datastore.Entity(key=portfolio_key)
        user_entry = [{'ticker':ticker, 'price':price, 'amount':amount, 'date':date}]
        user_portfolio["data"] = json.dumps(user_entry)
        print(user_portfolio["data"])
        ds_client.put(user_portfolio)
    # else this user has a portfolio, update it with this ticker
    else:
        user_entry = {'ticker':ticker, 'price':price, 'amount':amount, 'date':date}
        current_data = json.loads(user_portfolio["data"])
        current_data.append(user_entry)
        user_portfolio["data"] = json.dumps(current_data)
        print(user_portfolio["data"])
        ds_client.put(user_portfolio)

    return redirect("/profile")

@app.route("/profile/get", methods=["GET"])
def get_tickers_for_user():
    user = session.get("user", None)
    portfolio_key = ds_client.key("Portfolio", user)
    user_portfolio = ds_client.get(portfolio_key)

    if user_portfolio is None:
        return -1
    print(user_portfolio["data"])
    return user_portfolio["data"]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
