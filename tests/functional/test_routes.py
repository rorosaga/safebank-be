import pytest
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from iebank_api import app

# ACCOUNT TESTS
def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is created (POST)
    THEN check the account is created successfully
    """
    response = testing_client.post('/accounts', json={'name': 'New Account','country': 'Spain', 'username':'maggieyc'})
    assert response.status_code == 201
    assert response.json['account']['name'] == 'New Account'
    assert response.json['account']['currency'] == 'EUR'
    assert response.json['account']['country'] == 'Spain'

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 500


def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT)
    THEN check the account is updated successfully
    """
    # Create a new account first
    response = testing_client.post('/accounts', json={'name': 'New Account', 'country': 'Spain', 'username':'maggieyc'})
    assert response.status_code == 201
    account_id = response.json['account']['id']

    # Update the account's country and name
    response = testing_client.put(f'/accounts/{account_id}', json={'name': 'Test Updated','username':'maggieyc', 'country': 'France'})
    assert response.status_code == 200
    assert response.json['account']['name'] == 'Test Updated'
    assert response.json['account']['country'] == 'France'

def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is deleted (DELETE)
    THEN check the account is deleted successfully
    """
    # Create a new account first
    response = testing_client.post('/accounts',json={'name': 'Test', 'country': 'Canada', 'username':'maggieyc'})
    assert response.status_code == 201
    account_id = response.json['account']['id']

    # Delete the account
    response = testing_client.delete(f'/accounts/{account_id}')
    assert response.status_code == 200
    assert response.json['account']['id'] == account_id


# USER TESTS
def test_get_users(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/users')
    assert response.status_code == 200

def test_create_user(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users' page recieves (POST)
    THEN check the user is created successfully
    """
    response = testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'})
    assert response.status_code == 201
    assert response.json['user']['username'] == 'bob1234'
    assert response.json['user']['country'] == 'Canada'

def test_user_default_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users' page revieves (POST)
    THEN check that a default Account is created for the new User
    """
    
    testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'})
    response = testing_client.get('/userspace/bob1234/accounts')
    assert len(response.json['accounts']) == 1

def test_update_user(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users' page recieves (PUT)
    THEN check the user is updated successfully
    """
    response = testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'})
    assert response.status_code == 201

    response = testing_client.put('/users/bob1234', json={'country': 'Spain'})
    assert response.json['user']['username'] == 'bob1234'
    assert response.json['user']['country'] == 'Spain'


def test_delete_user(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/users' page revieves (DELETE)
    THEN check the user is deleted successfully
    """
    response = testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'})
    assert response.status_code == 201

    response = testing_client.delete('/users/bob1234')
    assert response.status_code == 200
    assert response.json['user']['username'] == 'bob1234'


# TRANSFER TESTS
def test_get_transactions(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/transactions' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/transactions')
    assert response.status_code == 200

def test_transfer(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/userspace/<username>/transfer' page revieves (PUT)
    THEN check the transfer is made successfully
    """
    testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'})
    testing_client.post('/accounts', json={'name': 'Account2', 'country':'Spain', 'username':'bob1234'})

    response = testing_client.get('/userspace/bob1234/accounts')
    accounts = response.json['accounts']
    assert len(accounts) == 2
    ids = [account['account_number'] for account in accounts]
    id1 = ids[0]
    id2 = ids[1]
    response = testing_client.put('/userspace/bob1234/transfer', json={'source':id1, 'target': id2, 'amount':"100", 'currency': 'EUR'})
    assert response.status_code == 200

def test_invalid_transfers(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/userspace/<username>/transfer' page revieves (PUT) with a negative amount, or the amount is too large
    THEN check the transfer is unsuccessful
    """
    testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'})
    testing_client.post('/accounts', json={'name': 'Account2', 'country':'Spain', 'username':'bob1234'})

    response = testing_client.get('/userspace/bob1234/accounts')
    accounts = response.json['accounts']
    assert len(accounts) == 2
    ids = [account['account_number'] for account in accounts]
    id1 = ids[0]
    id2 = ids[1]
    response = testing_client.put('/userspace/bob1234/transfer', json={'source':id1, 'target': id2, 'amount':"-100", 'currency': 'EUR'})
    assert response.status_code == 400
    response = testing_client.put('/userspace/bob1234/transfer', json={'source':id1, 'target': id2, 'amount':"10000", 'currency': 'EUR'})
    assert response.status_code == 400

def test_transfer_between_users(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/userspace/<username>/transfer' page revieves (PUT)
    THEN check the transfer is made successfully between different users
    """

    testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'})
    testing_client.post('/users', json={'username': 'maggie1234', 'country': 'Canada', 'password': '1234'})

    response = testing_client.get('/accounts')
    accounts = response.json['accounts']
    print(accounts)
    assert len(accounts) == 2
    ids = [account['account_number'] for account in accounts]
    id1 = ids[0]
    id2 = ids[1]
    response = testing_client.put('/userspace/bob1234/transfer', json={'source':id1, 'target': id2, 'amount':"100", 'currency': 'EUR'})
    assert response.status_code == 200


# LOGIN TESTS
def test_user_login(testing_client):
    testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'}) 
    response = testing_client.post('/clientlogin', json={'username': 'bob1234', 'password': '1234'})
    assert response.status_code == 200

def test_unsuccessful_user_login(testing_client):
    testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'}) 
    response = testing_client.post('/clientlogin', json={'username': 'bob1234', 'password': '4321'})
    assert response.status_code == 401

def test_existing_account(testing_client):
    testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'}) 
    response = testing_client.post('/users', json={'username': 'bob1234', 'country': 'Canada', 'password': '1234'}) 
    assert response.status_code == 400