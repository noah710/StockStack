from google.cloud import datastore
import json
import datetime
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

# blueprints
from profile import blueprint as profile_blueprint
from auth import blueprint as auth_blueprint
from api import blueprint as api_blueprint

ds_client = datastore.Client()

app = Flask(__name__)

# this causing problems on app engine
# need to make this static, https://stackoverflow.com/questions/51014992/google-app-engine-session-loses-attribute
app.secret_key = b'Vwqw\x9d)G\xb2\x00/\xb4b'

# handle all profile requests in profile.py
app.register_blueprint(profile_blueprint, url_prefix="/profile")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(api_blueprint, url_prefix="/api")

@app.route("/")
def home():
    """Return a simple HTML page."""
    print("Hit the route!")

    # check if there is an active session
    user = session.get("user", None)
    
    get_top_tickers()

    # add user variable to homepage
    data = get_default_dates_and_prices('SPY')
    return render_template("index.html", user = user, data = data)

@app.route("/curated_tickers", methods=['GET'])
def get_curated_tickers():
    # can make these dynamic later, load from file, or random generated
    tickers = ["MSFT", "TSLA", "AAPL", "GE", "AMZN", "NVDA", "FB", "AMD", "NFLX", "TWTR"]

    return jsonify(tickers) 

#puts only the tickers of the top gainers in an array and jsonifys it. 
@app.route("/top_tickers", methods=['GET'])      
def get_top_tickers():
    top_tickers = si.get_day_gainers()
    
    top_array = []
    
    for x in range(10):
        top_array.append((str(top_tickers['Symbol'][x])))
        
    return jsonify(top_array)
    
#puts only the tickers of the top losers in an array and jsonifys it.
@app.route("/bottom_tickers", methods=['GET'])      
def get_bottom_tickers():
    bottom_tickers = si.get_day_losers()
    
    bottom_array = []
    
    for x in range(10):
        bottom_array.append((str(bottom_tickers['Symbol'][x])))
        
    return jsonify(bottom_array)   

#puts only the tickers of the most active stocks in an array and jsonifys it.
@app.route("/active_tickers", methods=['GET'])      
def get_active_tickers():
    active_tickers = si.get_day_most_active()
    
    active_array = []
    
    for x in range(10):
        active_array.append((str(active_tickers['Symbol'][x])))
        
    return jsonify(active_array) 
     

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

    # retrieve query from search bar
    query = request.form.get("query")
    results = get_default_ticker_info(query)
    data = get_default_dates_and_prices(query)
    return render_template("results.html", query = results, data = json.dumps(data), user = user)

@app.route("/results/<ticker>", methods=["GET"])
def loadResults_get(ticker):

     # check if there is an active session
    user = session.get("user", None)

    # retrieve query from search bar
    query = ticker
    results = get_default_ticker_info(query)
    data = get_default_dates_and_prices(query)
    return render_template("results.html", query = results, data = json.dumps(data), user = user)

@app.route("/aboutus", methods=["GET"])
def about_us():

    user = session.get("user", None)

    return render_template("aboutus.html", user = user)

@app.route("/sendYF/<ticker>", methods=["GET"])
def fetch(ticker):
    # pull from yf_nasdaq db
    ticker_list = si.tickers_nasdaq()

    # calls for variation
    # Dow == si.tickers_dow()
    # S&P500 == si.tickers_sp500()
    # Others == si.tickers_other()

    # all tickers in currently selected list
    #print(ticker_list)

    #initialize and fill new array with data objects
    data = si.get_data(ticker)['open'][-1] # select last element of open column
    # !! this print causing an error
    #print("data = " + data)

    # nested for loop to fill data array
    #for x in range(0, len(ticker_list)-1):
    #    for ticker in ticker_list:
    #        dataArr[x] = si.get_data(ticker) # if there's multiple tickers here, dataArr[x] will be overwritten and only the last ticker will be stored at dataArr[x]
    #        print(dataArr[x])

    #for x in range(0, len(ticker_list)-1):
    #    for ticker in ticker_list:
            #dataArr[x] = si.get_data(ticker)
            #print(dataArr[0][0])

    # return jsonified data to script
    #print("printing data jsonified: " + str(jsonify(data)))

    #return jsonified data array
    
    # xmltodict is causing an error here, just gonna json the data
    #Data = xmltodict.parse(data)
    
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
