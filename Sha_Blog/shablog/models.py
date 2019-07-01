from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# now we're importing current_app instead of variable 'app'
# this is now application
from flask import current_app
from shablog import db, login_manager
from flask_login import UserMixin
from shablog.config import Constants


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# UserMixin -> This provides default implementations 
# for the methods that Flask-Login expects user objects to have.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default=Constants.DEFAULT_PROFILE_PICTURE)
    password = db.Column(db.String(60), nullable=False)
    # relationship -> user(author) : post = 1 : n
    post = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_seconds=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{ self.username }', '{ self.email }', '{ self.image_file }')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # utcnow -> we don't want that current time is the one right now,
    # which should be if we called utcnow(), 
    # we want to pass function as argument
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # user.id -> we are referencing a table name and NOT a Model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{ self.title }', '{ self.date_posted }')"
