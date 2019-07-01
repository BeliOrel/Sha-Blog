# if we want to save email username and password to environment variables
# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from shablog.config import Config, Constants

# app = Flask(__name__) <- removed to create_app()

# DB instance
# db = SQLAlchemy(app)
db = SQLAlchemy()
# bcrypt = Bcrypt(app)
bcrypt = Bcrypt()
# login_manager = LoginManager(app)
login_manager = LoginManager()
login_manager.login_view = Constants.LOGIN_VIEW  # function name of the route
login_manager.login_message_category = Constants.LOGIN_MESSAGE_CATEGORY  # bootstrap class
# mail = Mail(app)
mail = Mail()


# create app application
def create_app(config_class=Config):
    app = Flask(__name__)
    # as environment variables
    # app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from shablog.users.routes import users
    from shablog.posts.routes import posts
    from shablog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
