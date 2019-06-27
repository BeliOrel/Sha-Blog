from datetime import datetime 
from shablog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # relationship -> user(author) : post = 1 : n
    post = db.relationship('Post', backref='author', lazy=True)

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