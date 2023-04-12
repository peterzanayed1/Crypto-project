from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Coin, coin_schema, coins_schema, Closedtrans,closedtrans_schema,closedtranss_schema
import requests
from datetime import datetime


api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}


@api.route('/coin', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    coin_symbol = request.json['coin_symbol']
    amount = request.json['amount']
    purchase_price = request.json['purchase_price']
    purchase_date = request.json['purchase_date']
    user_token = current_user_token.token

  
    print(f'big tester {current_user_token.token}')

    coin = Coin(coin_symbol,amount,purchase_price,purchase_date,user_token=user_token)

    db.session.add(coin)
    db.session.commit()

    response = coin_schema.dump(coin)
    return jsonify(response)

@api.route('/coin', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Coin.query.filter_by(user_token = a_user).all()
    response = coins_schema.dump(contacts)
    return jsonify(response)

@api.route('/coins/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    fan = current_user_token
    if fan:
        coin = Coin.query.get(id)
        response = coin_schema.dump(coin)
        return jsonify(response)
    else:
        return jsonify({'message':'valid token required'}), 401
    
@api.route('/coins/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    coin = Coin.query.get(id)
    coin.coin_symbol = request.json['coin symbol']
    coin.amount = request.json['amount']
    coin.purchase_price = request.json['purchase_price']
    coin.purchase_date = request.json['purchase_date']
    coin.user_token = current_user_token.token

    db.session.commit()
    response = coin_schema.dump(coin)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token,id):
    coin = Coin.query.get(id)
    db.session.delete(coin)
    db.session.commit()
    response = coin_schema.dump(coin)
    return jsonify(response)



@api.route('/prices', methods=['GET'])
def get_prices():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '3b1418e5-aec7-4add-921e-4c65d1598c95'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    prices = {}

    for coin in data['data']:
        name = coin['name']
        symbol = coin['symbol']
        price = coin['quote']['USD']['price']
        market_cap = coin['quote']['USD']['market_cap']
        prices[symbol] = {'name': name, 'price': price, 'market_cap': market_cap, 'symbol': symbol}

    return jsonify(prices)

if __name__ == '__main__':
    api.run(debug=True)



@api.route('/rawdata', methods=['GET'])
def get_rawdata():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '3b1418e5-aec7-4add-921e-4c65d1598c95'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    return jsonify(data)


@api.route('/closedtrans/<id>', methods = ['DELETE'])
def closetrans(id):
    coin = Coin.query.get(id)
    
    # Fetch the rawdata API and get the price for the symbol
    response = requests.get("https://lemon-noisy-croissant.glitch.me/api/rawdata")
    data = response.json()["data"]
    symbol_price = {currency["symbol"]: currency["quote"]["USD"]["price"] for currency in data}
    
    # Get the sale price for the coin's symbol
    sale_price = symbol_price.get(coin.coin_symbol)
    if sale_price is None:
        return jsonify({"message": "Invalid coin symbol"})
    
    # Calculate the holding time and profit
    profit = (coin.amount * coin.purchase_price) - (coin.amount * sale_price)
    
    # Create a new row in the "closetrans" table with the necessary data
    closedtrans = Closedtrans(
        id=coin.id,
        coin_symbol=coin.coin_symbol,
        purchase_price=coin.purchase_price,
        amount=coin.amount,
        purchase_date=coin.purchase_date,
        sale_date=datetime.now(),
        sale_price=sale_price,
        holding_time="0",
        profit=profit
    )
    
    # Add the new row to the "closetrans" table
    db.session.add(closedtrans)
    
    # Delete the row from the original SQL table
    db.session.delete(coin)
    
    db.session.commit()
    response = coin_schema.dump(coin)
    return jsonify(response)