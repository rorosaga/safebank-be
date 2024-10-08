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

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={'name': 'John Doe', 'currency': '€', 'country': 'Spain'})
    assert response.status_code == 200

def test_create_account_invalid_data(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST) with invalid data
    THEN check the response returns a 400 status code
    """
    # Missing required 'name' and 'currency'
    response = testing_client.post('/accounts', json={'country': 'Spain'})
    assert response.status_code == 400

def test_update_account_invalid_data(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT) with invalid data
    THEN check the response returns a 400 status code
    """
    # Create a new account first
    response = testing_client.post('/accounts', json={'name': 'Bob', 'currency': 'USD', 'country': 'USA'})
    assert response.status_code == 200
    account_id = response.json['id']

    # Attempt to update with invalid data (e.g., missing 'name')
    response = testing_client.put(f'/accounts/{account_id}', json={'country': 'France'})
    assert response.status_code == 400


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
    response = testing_client.post('/accounts', json={'name': 'Jane Doe', 'currency': '$', 'country': 'USA'})
    assert response.status_code == 200
    account_id = response.json['id']

    # Now delete the account
    response = testing_client.delete(f'/accounts/{account_id}')
    assert response.status_code == 200

    # Check that the account no longer exists
    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 404

def test_delete_non_existent_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is deleted (DELETE) with a non-existent id
    THEN check the response returns a 404 status code
    """
    response = testing_client.delete('/accounts/9999')  # Non-existent ID
    assert response.status_code == 404
