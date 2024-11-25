
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from iebank_api.models import Account, User, Transaction
from iebank_api import db, app

@pytest.fixture
def testing_client(scope='module'):
    with app.app_context():
        db.create_all()
        account = Account('Test Account', '€', 'Spain', "John")
        db.session.add(account)
        db.session.commit()

    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.drop_all()