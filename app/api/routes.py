from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Coin, coin_schema, coins_schema
import requests


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
        prices[symbol] = {'name': name, 'price': price}

    return jsonify(prices)

if __name__ == '__main__':
    api.run(debug=True)

