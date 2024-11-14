from iebank_api import db
from datetime import datetime
import string, random
from werkzeug.security import generate_password_hash

class User(db.Model):
    username = db.Column(db.String(32), nullable=False, primary_key=True)
    password = db.Column(db.String(50), nullable=False ) # Added password

    # Establish relationship with Account
    accounts = db.relationship('Account', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.accounts = []

    # Returns all accounts associated with a User
    def get_accounts(self):
        return self.accounts

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default = 0.0)
    currency = db.Column(db.String(3), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    country = db.Column(db.String(64), nullable=False) # Added new country field
    # password = db.Column(db.String(50), nullable=False ) #Added password

    username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.account_number

    def __init__(self, name, currency, country, username):
        self.name = name
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.balance = 0.0
        self.status = "Active"
        self.country = country # Initialize country field
        self.username=username
        # self.password = generate_password_hash(password)

def get_user_by_username(username):
    return User.query.filter_by(name=username).first()