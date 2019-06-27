from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# secret key for aplication, so nobody can modify form data
app.config['SECRET_KEY'] = '4cb195a017b7d117311173f6d1635375'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# DB instance
db = SQLAlchemy(app)

from shablog import routes
