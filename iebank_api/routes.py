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
def create_account(data=None):
    if data == None:
        data = request.json
    name = data.get('name')
    country = data.get('country')
    username = data.get('username')
    #password = data.get('password')
    # Create a new account with the hashed password
    account = Account(name=name, currency='EUR', country=country, username=username)
    db.session.add(account)
    db.session.commit()

    return jsonify({'message': 'Account created successfully', 'account': format_account(account)}), 201


#the signup routes
@app.route('/clientsignup')
def client_signup():
    return "Client Signup Page"  


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return {'accounts': [format_user(user) for user in users]}


@app.route('/accounts', methods=['GET'])
def get_accounts():
    """
    Fetch all user accounts from the database.
    This is for debugging purposes and includes sensitive data like hashed passwords.
    DO NOT USE in production!
    """
    try:
        # Query all users from the User table
        accounts = Account.query.all()

        # Format the user data
        accounts = [format_account(account) for account in accounts]

        # Return the response
        return {'accounts': accounts}

    except Exception as e:
        # Handle unexpected errors
        print(f"Error fetching accounts: {e}")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


# Helper function to format user data
def format_user(user):
    """
    Format user data for debugging purposes.
    Includes sensitive information (hashed passwords).
    """
    return {
        'id': user.id,
        'username': user.username,
        'password': user.password  # Include hashed password for debugging
    }


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
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400

        hashed_password = generate_password_hash(password)

        # Debugging
        print(f"Signup - Raw password: {password}")
        print(f"Signup - Hashed password before saving: {hashed_password}")

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Automatically create a bank account for the user

        new_account = Account(
            name=f"{username}'s Account",  # Set default name
            currency="$",                 # Default currency
            country="Spain",                # Default country 
            username=username             # Associate with the user
        )
        db.session.add(new_account)
        db.session.commit()

        # Fetch back the stored hash
        stored_user = User.query.filter_by(username=username).first()
        print(f"Stored hash in database: {stored_user.password}")


        return jsonify({'message': 'User created successfully and account opened!'}), 201

    except Exception as e:
        print(f"Error during user creation: {e}")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


# Login code

@app.route('/clientlogin', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        user = User.query.filter_by(username=username).first()

        # Debugging
        print(f"Login - Username: {username}")
        print(f"Login - Raw password provided: {password}")
        if user:
            print(f"Login - Stored hashed password from database: {user.password}")
            print(f"Hash comparison result: {check_password_hash(user.password, password)}")

        if user and check_password_hash(user.password, password):
            return jsonify({'message': 'Login successful'}), 200

        return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


# Transactions code

@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions = Transaction.query.all()
    return {"transactions": [format_transaction(transaction) for transaction in transactions]}, 200


@app.route('/userspace/<string:username>/accounts', methods=['GET'])
def get_user_accounts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    accounts = user.get_accounts()  # Calls the method in your User model
    return jsonify({
        "accounts": [
            {
                "username": account.username,
                "name": account.name,
                "account_number": account.account_number,
                "balance": account.balance,
                "currency": account.currency,
                "country": account.country,
                "status": account.status,
                "created_at": account.created_at.isoformat(),
            }
            for account in accounts
        ]
    }), 200



@app.route('/userspace/<string:username>/transactions', methods=['GET'])
def get_user_transactions(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "User not found"}, 404
    
    transactions = user.get_transactions()
    return {"transactions": [format_transaction(transaction) for transaction in transactions]}, 200

@app.route('/userspace/<string:username>/transfer', methods=['PUT'])
def transfer_money(username):
    try:
        # Fetch the user making the transfer
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Extract and validate the request data
        data = request.json
        source_id = data.get('source')
        target_id = data.get('target')
        currency = data.get('currency')
        try:
            amount = float(data.get('amount'))
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid amount value'}), 400

        # Validate source account
        source_account = Account.query.filter_by(account_number=source_id).first()
        if not source_account:
            return jsonify({'message': 'Source account not found'}), 404
        if source_account.username != user.username:
            return jsonify({'message': 'Source account does not belong to the user'}), 403
        if source_account.balance < amount:
            return jsonify({'message': 'Insufficient funds in source account'}), 400

        # Validate target account
        target_account = Account.query.filter_by(account_number=target_id).first()
        if not target_account:
            return jsonify({'message': 'Target account not found'}), 404

        # Perform the transfer
        source_account.balance -= amount
        target_account.balance += amount
        db.session.commit()

        # Log the transaction
        transaction = Transaction(
            username=username,
            currency=currency,
            source_account=source_id,
            target_account=target_id,
            amount=amount
        )
        db.session.add(transaction)
        db.session.commit()

        # Return success response
        return jsonify({
            'message': 'Transfer successful',
            'source_account': {
                'account_number': source_account.account_number,
                'balance': source_account.balance,
                'currency': source_account.currency
            },
            'target_account': {
                'account_number': target_account.account_number,
                'balance': target_account.balance,
                'currency': target_account.currency
            }
        }), 200

    except Exception as e:
        # Handle unexpected errors1
        print(f"Error during transfer: {e}")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


    # Check if amount is positive
    if amount <= 0:
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