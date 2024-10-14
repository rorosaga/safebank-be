from iebank_api import app
import pytest

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
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'})
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe'
    assert response.json['currency'] == '€'
    assert response.json['country'] == 'Spain'

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404


def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT)
    THEN check the account is updated successfully
    """
    # Create a new account first
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'})
    assert response.status_code == 200
    account_id = response.json['id']

    # Update the account's country and name
    response = testing_client.put(f'/accounts/{account_id}', json={'name': 'John Doe Updated', 'country': 'France'})
    assert response.status_code == 200
    assert response.json['name'] == 'John Doe Updated'
    assert response.json['country'] == 'France'

def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is deleted (DELETE)
    THEN check the account is deleted successfully
    """
    # Create a new account first
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'})
    assert response.status_code == 200
    account_id = response.json['id']

    # Delete the account
    response = testing_client.delete(f'/accounts/{account_id}')
    assert response.status_code == 200
    assert response.json['id'] == account_id