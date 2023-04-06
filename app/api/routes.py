from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, contact_schema, contacts_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}


@api.route('/cars', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token

  
    print(f'big tester {current_user_token.token}')

    car = Car(make,model,year,color,user_token=user_token)

    db.session.add(car)
    db.session.commit()

    response = contact_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Car.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    fan = current_user_token
    if fan:
        contact = Car.query.get(id)
        response = contact_schema.dump(contact)
        return jsonify(response)
    else:
        return jsonify({'message':'valid token required'}), 401
    
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    contact = Car.query.get(id)
    contact.make = request.json['make']
    contact.model = request.json['model']
    contact.year = request.json['year']
    contact.color = request.json['color']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token,id):
    contact = Car.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)
