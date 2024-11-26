from iebank_api import app
from flask import Flask, send_from_directory
import os

if __name__ == '__main__':
    app.run(debug=True)