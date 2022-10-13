import os
import sys  

scripts_path = ""
if os.uname().sysname.find("Win") > -1:
    sys.path.insert(0, os.getcwd() + "\\OraIVWebApp")
    scripts_path = os.getcwd() + "\\OraIVWebapp\\scripts"
    sys.path.insert(0, scripts_path )
else:
    sys.path.insert(0, os.getcwd() + "/OraIVWebApp")
    sys.path.insert(0, os.getcwd())
    scripts_path = os.getcwd() + "/OraIVWebApp/scripts"
    sys.path.insert(0, scripts_path)

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Uses __init__.py file for app configuration
app.config.from_object('config')
#db = SQLAlchemy(app)

from OraIVWebApp import views
