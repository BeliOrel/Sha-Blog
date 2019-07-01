# if we want to save email username and password to environment variables
# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from shablog.constants import SQLALCHEMY_DATABASE_URI, SECRET_KEY, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, LOGIN_VIEW, LOGIN_MESSAGE_CATEGORY, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)

# secret key for aplication, so nobody can modify form data
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

# as environment variables
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

mail = Mail(app)

# DB instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = LOGIN_VIEW  # function name of the route
login_manager.login_message_category = LOGIN_MESSAGE_CATEGORY  # bootstrap class

from shablog import routes
