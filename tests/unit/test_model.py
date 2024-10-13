from iebank_api.models import Account
import pytest

def test_create_account():
    """
    GIVEN a Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, status and created_at fields are defined correctly
    """
    account = Account('John Doe', '€', 'Spain')
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.account_number != None
    assert account.country == 'Spain'
    assert account.balance == 0.0
    assert account.status == 'Active'

def test_create_account_with_country():
    """
    GIVEN an Account model
    WHEN a new Account is created with a country
    THEN check the name, account_number, balance, currency, status, created_at, and country fields are defined correctly
    """
    account = Account('John Doe', '€', 'Spain')
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.account_number is not None
    assert account.balance == 0.0
    assert account.status == 'Active'
    assert account.country == 'Spain'

def test_account_number_generation():
    """
    GIVEN an Account model
    WHEN a new Account is created
    THEN check that account_number is a string of 20 digits
    """
    account = Account('Jane Doe', '€', 'France')
    assert len(account.account_number) == 20
    assert account.account_number.isdigit()

def test_default_balance_and_status():
    """
    GIVEN an Account model
    WHEN a new Account is created
    THEN check that the balance and status have default values
    """
    account = Account('Alice', '$', 'USA')
    assert account.balance == 0.0
    assert account.status == 'Active'

def test_account_without_country():
    """
    GIVEN an Account model
    WHEN a new Account is created without a country
    THEN check that it raises an error
    """
    with pytest.raises(TypeError):
        account = Account('John Doe', '€')  # Missing 'country' argument

def test_account_initialization_with_balance():
    """
    GIVEN an Account model
    WHEN a new Account is created with a specific balance
    THEN check that the balance is set correctly
    """
    account = Account('Jane Doe', '$', 'USA')
    account.balance = 100.0  # Manually setting balance
    assert account.balance == 100.0
