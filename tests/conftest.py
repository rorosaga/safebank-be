import sys
import os
import pytest
import sys
import os

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from iebank_api.models import Account, User, Transaction
from iebank_api import db, app


@pytest.fixture
def testing_client(scope='module'):
    with app.app_context():
        db.create_all()

        user = User('maggieyc', '1234', 'Canada')
        #account = Account('Test Account', 'EUR', 'Canada', "maggieyc")
        db.session.add(user)
        #db.session.add(account)
        db.session.commit()

    with app.test_client() as testing_client:
        yield testing_client

    with app.app_context():
        db.drop_all()
