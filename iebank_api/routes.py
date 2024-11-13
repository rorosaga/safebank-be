from flask import request, jsonify
from iebank_api import db, app  
from iebank_api.models import Account, get_user_by_username
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/skull', methods=['GET'])
def skull():
    text = 'Hi! This is the BACKEND SKULL! 💀 '
    
    text = text +'<br/>Database URL:' + db.engine.url.database
    if db.engine.url.host:
        text = text +'<br/>Database host:' + db.engine.url.host
    if db.engine.url.port:
        text = text +'<br/>Database port:' + db.engine.url.port
    if db.engine.url.username:
        text = text +'<br/>Database user:' + db.engine.url.username
    if db.engine.url.password:
        text = text +'<br/>Database password:' + db.engine.url.password
    return text

@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.json
    name = data.get('name')
    country = data.get('country')
    password = data.get('password')

    if not name or not country or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if the username already exists
    if Account.query.filter_by(name=name).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Create a new account with the hashed password
    account = Account(name=name, currency='EUR', country=country, password=hashed_password)
    db.session.add(account)
    db.session.commit()

    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/clientlogin', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_username(username) 
    
    if user:   
        if user and check_password_hash(user.password, password): 
            return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/clientsignup')
def client_signup():
    return "Client Signup Page"  


@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return {'accounts': [format_account(account) for account in accounts]}

@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = Account.query.get(id)
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    account.name = request.json['name']
    account.country = request.json['country']
    db.session.commit()
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    return format_account(account)

def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'status': account.status,
        'created_at': account.created_at,
        'country': account.country # Return country field also
 
    }