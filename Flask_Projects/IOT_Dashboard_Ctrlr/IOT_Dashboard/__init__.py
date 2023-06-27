import os, sys


from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Uses __init__.py file for app configuration
#app.config.from_object('config')
#db = SQLAlchemy(app)

from IOT_Dashboard import views
