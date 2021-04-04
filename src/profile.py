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

@blueprint.route("/add", methods=["POST"])
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

@blueprint.route("/get", methods=["GET"])
def get_tickers_for_user():
    user = session.get("user", None)
    portfolio_key = ds_client.key("Portfolio", user)
    user_portfolio = ds_client.get(portfolio_key)

    if user_portfolio is None:
        return -1
    print(user_portfolio["data"])
    return user_portfolio["data"]
    