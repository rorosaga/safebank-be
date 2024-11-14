from flask import request, jsonify
from iebank_api import db, app  
from iebank_api.models import Account, User, Transaction, get_user_by_username
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
    username = data.get('username')
    #password = data.get('password')

    '''
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
    '''

    # Create a new account with the hashed password
    account = Account(name=name, currency='EUR', country=country, username=username)
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

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    password = data.get('password')
    username = data.get('username')

    
    if not username or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if the username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Create a new account with the hashed password
    account = User(username=username, password=hashed_password)
    db.session.add(account)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/user/<string:username>')
def get_user(username):
    user = User.query.filter_by(username=username).first()
    return format_user(user), 200

@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions = Transaction.query.all()
    return {"transactions": [format_transaction(transaction) for transaction in transactions]}, 200


@app.route('/userspace/<string:username>/accounts', methods=['GET'])
def get_user_accounts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "User not found"}, 404
    accounts = user.get_accounts()
    return {"accounts": [format_account(account) for account in accounts]}, 200


@app.route('/userspace/<string:username>/transactions', methods=['GET'])
def get_user_transactions(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "User not found"}, 404
    
    transactions = user.get_transactions()
    return {"transactions": [format_transaction(transaction) for transaction in transactions]}, 200

@app.route('/userspace/<string:username>/transfer', methods=['PUT'])
def transfer_money(username):
    user = User.query.filter_by(username=username).first()
    source_id = request.json['source']
    target_id = request.json['target']
    currency = request.json['currency']
    try:
        amount = float(request.json.get('amount'))
    except ValueError:
        return jsonify({'message': 'Invalid amount value'}), 400


    
    # Check if source account belongs to the user
    source_account = Account.query.filter_by(account_number=source_id).first()
    if not source_account:
        return jsonify({'message': 'Source account not found'}), 404

    # Ensure the source account is associated with the user
    if source_account.username != user.username:
        return jsonify({'message': 'Source account does not belong to the user'}), 400

    # Check if target account exists
    target_account = Account.query.filter_by(account_number=target_id).first()
    if not target_account:
        return jsonify({'message': 'Target account not found'}), 404

    # Perform the transfer (assuming basic checks on balance)
    if source_account.balance < float(amount):
        return jsonify({'message': 'Insufficient funds'}), 400

    # Update balances
    source_account.balance -= float(amount)
    target_account.balance += float(amount)
    
    # Commit the changes to the database
    db.session.commit()

    # Log transaction
    transaction = Transaction(
        username=username,
        source_account=source_id,
        target_account=target_id,
        currency=currency,  # Adjust if currency field needs to be dynamic
        amount=amount
    )
    db.session.add(transaction)

    db.session.commit()

    # Return success response with updated account details
    return jsonify({
        'message': 'Transfer successful',
        'source_account': format_account(source_account),
        'target_account': format_account(target_account)
    }), 200

def format_account(account):
    return {
        'id': account.id,
        'username': account.username,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'status': account.status,
        'created_at': account.created_at,
        'country': account.country # Return country field also
 
    }

def format_user(user):
    if user:
        return {
            "username": user.username,
        }
    else:
        return {"message": "User not found"}
    

def format_transaction(trans):
    return {
        "id": trans.id,
        "username": trans.username,
        "source_account": trans.source_account,
        "target_account": trans.target_account,
        "currency": trans.currency,
        "amount": trans.amount,
        "created_at": trans.created_at.isoformat()
    }