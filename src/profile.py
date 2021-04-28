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
    if len(entries) == 0:
        return jsonify([{'price':0, 'date': '0-0'}])

    # set quantities so we can lookup by ticker later
    quantities = {}
    # lets use yf.download to download them zoom zoom
    # this will also handle case where ticker !exist. If ticker !exist, values will be NaN
    tickers = ""
    for asset in entries:
        quantities.update({asset.get('ticker').upper(): asset.get('amount')})
        tickers += asset.get('ticker') + " " # string will look like "AAPL GME GE F "


    # generate string for download request
    
    raw_data = yf.download(tickers, period="1mo", interval="1d") 

    # time to calculate net worth at each day and create chart data object
    # this will hold the data to plot like this
    # chart_data = [
    #               {"price": price, "date": date},
    #               {"price": price, "date": date},
    #               ... ]
    chart_data = []
    # get each series
    for index, date in enumerate(raw_data.index):

        str_date = str(date).split(" ")[0]
        values = raw_data['Close'].iloc[index]
        
        day_total = 0.0 # will be net worth on this day
        # get each ticker in this series
        for key in quantities.keys():
            if type(values) is numpy.float64:
                price = float(values)
            else:
                price = float(values.get(key)) # get price of stock on that day from dataframe
            
            # check if price is NaN, this happens when tickers are invalid
            if price != price:
                continue

            asset_value = price * float(quantities.get(key)) # multiply price by amount of stock held
            
            day_total += asset_value
        
        # now that we have a date and total value for this day, add as x,y to chart_data
        chart_data.append({
            "price" : day_total,
            "date" : str_date
        })

    return jsonify(chart_data)
