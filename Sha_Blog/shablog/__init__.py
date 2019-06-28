from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from shablog.constants import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

# secret key for aplication, so nobody can modify form data
app.config['SECRET_KEY'] = '4cb195a017b7d117311173f6d1635375'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# DB instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # function name of the route
login_manager.login_message_category = 'info'  # bootstrap class

from shablog import routes
