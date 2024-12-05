from iebank_api.models import Account, User, Transaction
import pytest
from iebank_api import db

# ACCOUNT MODEL TESTS
def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    account = Account(name="Test",currency='€', country='Spain', username="John")
    assert account.name == 'Test'
    assert account.currency == '€'
    assert account.account_number != None
    assert account.country == 'Spain'
    assert account.balance == 1000.0
    assert account.status == 'Active'
    assert account.username == 'John'

def test_account_number_generation():
    """
    GIVEN an Account model
    WHEN a new Account is created
    THEN check that account_number is a string of 20 digits
    """
    account = Account(name="Test",currency='€', country='Spain', username="John")
    assert len(account.account_number) == 20
    assert account.account_number.isdigit()

def test_default_balance_and_status():
    """
    GIVEN an Account model
    WHEN a new Account is created
    THEN check that the balance and status have default values
    """
    account = Account(name="Test",currency='€', country='Spain', username="John")
    assert account.balance == 1000.0
    assert account.status == 'Active'

def test_account_without_country():
    """
    GIVEN an Account model
    WHEN a new Account is created without a country
    THEN check that it raises an error
    """
    with pytest.raises(TypeError):
            account = Account(name="Test",currency='€', username="John")

def test_account_initialization_with_balance():
    """
    GIVEN an Account model
    WHEN a new Account is created with a specific balance
    THEN check that the balance is set correctly
    """
    account = Account(name="Test",currency='€', country='Spain', username="John")
    account.balance = 100.0  # Manually setting balance
    assert account.balance == 100.0

# USER MODEL TESTS
def test_user_initialization():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that the username, password, and country are set correctly
    """
    user = User(username="john_doe", password="password123", country="Spain")
    
    assert user.username == "john_doe"
    assert user.password is not None  # Password is hashed, so we check that it is not None
    assert user.country == "Spain"


# TRANSACTION MODEL TESTS

def test_transaction_initialization():
    """
    GIVEN a Transaction model
    WHEN a new Transaction is created
    THEN check that the transaction details are set correctly
    """
    transaction = Transaction(username="john_doe", currency="€", source_account="12345678901234567890", target_account="09876543210987654321", amount=100.0)
    
    assert transaction.username == "john_doe"
    assert transaction.currency == "€"
    assert transaction.source_account == "12345678901234567890"
    assert transaction.target_account == "09876543210987654321"
    assert transaction.amount == 100.0