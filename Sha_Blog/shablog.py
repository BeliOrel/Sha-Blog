from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# secret key for aplication, so nobody can modify form data
app.config['SECRET_KEY'] = '4cb195a017b7d117311173f6d1635375'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# DB instance
db = SQLAlchemy(app)


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


posts = [
    {
        'author': 'Corey Bee',
        'title': 'Blog Post 1',
        'content': 'First post content.',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Mei Honey',
        'title': 'Blog Post 2',
        'content': 'Second post content.',
        'date_posted': 'April 25, 2018'
    },
    {
        'author': 'Corey Bee',
        'title': 'Blog Post 3',
        'content': 'Third post content.',
        'date_posted': 'May 20, 2018'
    }
]

# you can have more than one route
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data }!', 'success')
        return redirect(url_for('home'))  # redirect to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password!', 'danger')
    return render_template('login.html', title='Login', form=form)


# if we don't want to use environment variables
# for a debug mode, we can also write
if __name__ == '__main__':
    app.run(debug=True)
