from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

app = Flask(__name__)


print(f"ENV is set to: {os.getenv('ENV')}") #can be removed after
# Select environment based on the ENV environment variable
if os.getenv('ENV') == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    print("Running in github mode")
    app.config.from_object('config.GithubCIConfig')
elif os.getenv('ENV') == 'uat':
    print("Running in uat mode")
    app.config.from_object('config.UATConfig')
elif os.getenv('ENV') == 'prod':
    print("Running in prod mode")
    app.config.from_object('config.PRODConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "*"}})

from iebank_api.models import Account, User, Transaction

with app.app_context():
    db.create_all()


from iebank_api import routes

