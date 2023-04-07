from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets


# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    


class Coin(db.Model):
    id = db.Column(db.String, primary_key = True)
    coin_symbol = db.Column(db.String(150), nullable = False)
    amount = db.Column(db.String(200))
    purchase_price = db.Column(db.String(20))
    purchase_date = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,coin_symbol,amount,purchase_price,purchase_date,user_token, id = ''):
        self.id = self.set_id()
        self.coin_symbol = coin_symbol
        self.amount = amount
        self.purchase_price = purchase_price
        self.purchase_date = purchase_date
        self.user_token = user_token


    def __repr__(self):
        return f'The following contact has been added to the phonebook: {self.make} models.py'

    def set_id(self):
        return (secrets.token_urlsafe())

class CoinSchema(ma.Schema):
    class Meta:
        fields = ['coin_symbol', 'amount','purchase_price','purchase_date', 'color',]

coin_schema = CoinSchema()
coins_schema = CoinSchema(many=True)