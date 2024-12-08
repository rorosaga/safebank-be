import os
import urllib.parse
from azure.identity import DefaultAzureCredential

class Config(object): 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/local.db'
    DEBUG = True

class GithubCIConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    DEBUG = True

class UATConfig(Config):
    if os.getenv('ENV') == 'uat':
        credential = DefaultAzureCredential()
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=urllib.parse.quote(os.getenv('DBUSER')),
            dbpass=credential.get_token(
                'https://ossrdbms-aad.database.windows.net').token,
            dbhost=os.getenv('DBHOST'),
            dbname=os.getenv('DBNAME')
        )

class DevelopmentConfig(Config):
    if os.getenv('ENV') == 'dev':

        # Initialize Azure credentials
        credential = DefaultAzureCredential()
        
        # Construct the SQLAlchemy Database URI
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=urllib.parse.quote(os.getenv('DBUSER')),
            dbpass=credential.get_token(
                'https://ossrdbms-aad.database.windows.net').token,
            dbhost=os.getenv('DBHOST'),
            dbname=os.getenv('DBNAME')
        )
        
        # Enable debugging
        DEBUG = True

class PRODConfig(Config):
    if os.getenv('ENV') == 'prod':

        # Initialize Azure credentials
        credential = DefaultAzureCredential()
        
        # Construct the SQLAlchemy Database URI
        SQLALCHEMY_DATABASE_URI = 'postgresql://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
            dbuser=urllib.parse.quote(os.getenv('DBUSER')),
            dbpass=credential.get_token(
                'https://ossrdbms-aad.database.windows.net').token,
            dbhost=os.getenv('DBHOST'),
            dbname=os.getenv('DBNAME')
        )

        # Disable debugging
        DEBUG = False
