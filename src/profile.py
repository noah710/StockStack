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
    Blueprint,
    escape
)

import yfinance as yf

# regex for sanitizing
import re

import json
import numpy

from google.cloud import datastore

blueprint = Blueprint('profile', __name__)

ds_client = datastore.Client()

@blueprint.route("/", methods=["GET"])
def profile():
    # load the user from the session
    user = session.get("user", None)

    if user is None:
        return redirect("/")
    else:
        return render_template("profile.html", user = user)

@blueprint.route("/add_ticker", methods=["POST"])
def add_to_portfolio():
    user = session.get("user", None)
    portfolio_key = ds_client.key("Portfolio", user)

    ticker = request.form.get("ticker")
    price = float(request.form.get("price"))
    amount = float(request.form.get("amount"))
    date = request.form.get("date")


    # check if the user has a portfolio
    user_portfolio = ds_client.get(portfolio_key)
    #if this user has no portfolio, make a new one for user and update
    if user_portfolio is None:
        user_portfolio = datastore.Entity(key=portfolio_key)
        user_entry = [{'ticker':ticker, 'price':str(price), 'amount':str(amount), 'date':date}]
        user_portfolio["data"] = json.dumps(user_entry)
        print(user_portfolio["data"])
        ds_client.put(user_portfolio)
    # else this user has a portfolio, update it with this ticker
    else:
        current_data = json.loads(user_portfolio["data"])

        # check if user is holding that stock already
        filtered = list(filter(lambda entry: entry['ticker'] == ticker, current_data))
        if len(filtered) == 1: # this can only be either 1 or 0, because there will never be duplicate stonks
            new_amount = float(filtered[0]['amount']) + amount
            new_price = (float(filtered[0]['amount'])*float(filtered[0]['price']) + price*amount)/new_amount # cost average
            # bad, but find ticker again to replace necessary fields
            for entry in current_data:
                if entry["ticker"] == ticker:
                    entry['amount'] = str(new_amount)
                    entry['price'] = str(round(new_price,2))
        else: # else this is a new stock and we can just add it
            user_entry = {'ticker':ticker, 'price':str(price), 'amount':str(amount), 'date':date}
            current_data.append(user_entry)

        # recreate portfolio json to store
        user_portfolio["data"] = json.dumps(current_data)
        print(user_portfolio["data"])
        ds_client.put(user_portfolio)

    return redirect("/profile")

@blueprint.route("/portfolio", methods=["GET"])
def get_tickers_for_user():
    user = session.get("user", None)
    portfolio_key = ds_client.key("Portfolio", user)
    user_portfolio = ds_client.get(portfolio_key)

    if user_portfolio is None:
        return -1
    print(user_portfolio["data"])
    return jsonify(json.loads(user_portfolio["data"]))

@blueprint.route("/remove_ticker/<ticker>", methods=["GET"])
def remove_ticker_button(ticker):
    user = session.get("user", None)
    portfolio_key = ds_client.key("Portfolio", user)

    # load in users portfolio
    user_portfolio = ds_client.get(portfolio_key)
    entries = json.loads(user_portfolio["data"])

    # look for and remove ticker
    for i, entry in enumerate(entries):
        if entry["ticker"] == ticker:
            entries.pop(i)
            user_portfolio["data"] = json.dumps(entries)
            print("Removed ticker {} from position {} from user {}".format(ticker, i, user))
            # update db
            ds_client.put(user_portfolio)
            return redirect("/profile")


    return jsonify(success=False)

@blueprint.route("/chart", methods=["GET"])
def generate_chart_data():
    user = session.get("user", None)

    # retrieve portfolio object
    portfolio_key = ds_client.key("Portfolio", user)
    user_portfolio = ds_client.get(portfolio_key)
    entries = json.loads(user_portfolio['data'])

    # EDGE: if users portfolio is empty, return 0's so the chart can display 0
    if len(entries) == 0: 
        return jsonify([{'price':0, 'date': '0-0'}])

    # set quantities so we can lookup by ticker later
    quantities = {}

    # string base for download request
    request_tickers = ""
    for asset in entries:
        # we will use this lookup how much of each ticker we have with the quantities dict
        quantities.update({asset.get('ticker').upper(): asset.get('amount')})
        
        # lets use yf.download to retrieve data faster. This appends the ticker to the request string
        # EDGE: this will also handle case where ticker !exist. If ticker !exist, values will be NaN
        request_tickers += asset.get('ticker') + " " # string will look like "AAPL GME GE F "

    # request data on all tickers simultaneously 
    raw_data = yf.download(request_tickers, period="1mo", interval="1d") # TODO: hardcoding period and intervals, maybe make these dyamic? 

    # time to calculate net worth at each day and create chart data object
    # this will hold the data to plot like this
    # chart_data = [ {"price": price, "date": date}, ... ]
    chart_data = []
    # iterate over data 1 day at a time
    for index, date in enumerate(raw_data.index):

        # get day for iteration
        str_date = str(date).split(" ")[0]

        # get array of price values for each stock on this day(index)
        values = raw_data['Close'].iloc[index]
        
        # sum net worth on this day
        day_total = 0.0

        # get each ticker's price on this day
        # quantities is a dict like: {'TICKER_NAME' : amount_owned}
        # values is a dict like {'TICKER_NAME' : price}
        for key in quantities.keys():
            # EDGE: if there is only 1 stock in portfolio, values will be a float instead of an array
            if type(values) is numpy.float64:
                price = float(values)
            else:
                # get price of ticker(key) on that day(values) from dataframe
                price = float(values.get(key)) 
            
            # check if price is NaN, this happens when tickers are invalid
            if price != price:
                # just going to continue and not include it in the net worth to be consistent with frontend logic
                continue
            
            # multiply price by amount of stock held
            asset_value = price * float(quantities.get(key)) 
            
            # increment day_total with value of this stock
            day_total += asset_value
        
        # now that we have a date and total value for this day, add as x,y to chart_data
        chart_data.append({
            "price" : day_total,
            "date" : str_date
        })

    return jsonify(chart_data)
