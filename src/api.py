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

import yfinance as yf

from google.cloud import datastore

blueprint = Blueprint('api', __name__)

ds_client = datastore.Client()

@blueprint.route("/ticker_price_change/<ticker>", methods=['GET'])
def get_price_change(ticker):
    ### Input: string ticker
    ### Output: json numpy.float64 price : positive if GREEN, negative if RED

    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history()
    current_price = round(data.tail(1)['Close'].iloc[0], 2) # this gets the last close price and rounds to 2 decimal places

    # if the current price is lower than last close price, send as negative so JS knows to make red
    if current_price < round(data.tail(2)['Close'].iloc[0], 2):
        current_price *= -1

    return jsonify(current_price)

@blueprint.route("/ticker_price/<ticker>", methods=['GET'])
def get_price(ticker):
    ### Input: string ticker
    ### Output: json numpy.float64 price


    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history()
    try:
        current_price = round(data.tail(1)['Close'].iloc[0], 2) # this gets the last close price and rounds to 2 decimal places
    except:
        return jsonify(0)
    return jsonify(current_price)
    