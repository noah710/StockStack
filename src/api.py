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

@blueprint.route("/ticker_price/<ticker>", methods=['GET'])
def get_price(ticker):
    ### Input: string ticker
    ### Output: json numpy.float64 price

    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history()
    current_price = round(data.tail(1)['Close'].iloc[0], 2) # this gets the last close price and rounds to 2 decimal places

    return jsonify(current_price)