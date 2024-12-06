from iebank_api import db
from datetime import datetime
import string
import random
from werkzeug.security import generate_password_hash
from sqlalchemy import func


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False, default="€")
    amount = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())

    username = db.Column(db.String(32), db.ForeignKey('user.username'), nullable=False)
    source_account = db.Column(db.String(20), db.ForeignKey('account.account_number'), nullable=False)
    target_account = db.Column(db.String(20), db.ForeignKey('account.account_number'), nullable=False)

    source = db.relationship('Account', foreign_keys=[source_account], backref='outgoing_transactions')
    target = db.relationship('Account', foreign_keys=[target_account], backref='incoming_transactions')

    def __repr__(self):
        return f'<Transaction {self.id}>'

    def __init__(self, username, currency, source_account, target_account, amount):
        self.username = username
        self.currency = currency
        self.source_account = source_account
        self.target_account = target_account
        self.amount = amount

    def get_account_transactions(account_number):
        """
        Returns all transactions associated with a bank account.

        :param account_number: The account number to query transactions for.
        :return: A list of transactions where the account is either the source or target.
        """
        return Transaction.query.filter(
            (Transaction.source_account == account_number) | 
            (Transaction.target_account == account_number)
        ).all()



class User(db.Model):
    username = db.Column(db.String(32), nullable=False, primary_key=True)
    password = db.Column(db.String(500), nullable=False)  
    country = db.Column(db.String(64), nullable=False)

    accounts = db.relationship('Account', backref='user', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, username, password, country):
        self.username = username
        self.password = password  # Assume pre-hashed password
        self.country = country

    def get_accounts(self):
        return Account.query.filter_by(username=self.username).all()


    def get_transactions(self):
        """
        Returns all transactions associated with the user's accounts.
        """
        account_numbers = [account.account_number for account in self.accounts]
        transactions = Transaction.query.filter(
            (Transaction.source_account.in_(account_numbers)) |
            (Transaction.target_account.in_(account_numbers))
        ).all()
        return transactions


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=1000.0)
    currency = db.Column(db.String(3), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    country = db.Column(db.String(64), nullable=False)

    username = db.Column(db.String(32), db.ForeignKey('user.username'), nullable=False)

    def get_accounts(username):
        return Account.query.filter_by(username=username)

    def __repr__(self):
        return f'<Account {self.account_number}>'

    def __init__(self, name, currency, country, username):
        self.name = name
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.country = country
        self.username = username
        self.balance = 1000.0
        self.status='Active'


def get_user_by_username(username):
    """
    Fetches a user by their username.
    """
    return User.query.filter_by(username=username).first()
