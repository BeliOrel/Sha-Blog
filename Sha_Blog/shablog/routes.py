import os
import secrets # for picture's name
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
# so we can use routes, DB and bcrypt -> @app
from shablog import app, db, bcrypt
from shablog.constants import PATH_PROFILE_PICTURE, DEFAULT_PROFILE_PICTURE
from shablog.forms import RegistrationForm, LoginForm, UpdateAccount
from shablog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))  # redirect to home page
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # if there exist 'next' parameter, then server should
            # redirect to that next page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    rand_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_file_name = rand_hex + f_ext
    picture_path = os.path.join(app.root_path, PATH_PROFILE_PICTURE, picture_file_name)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_file_name


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        # picture is not required
        if form.picture.data:
            # check if default profile picture
            if current_user.image_file != DEFAULT_PROFILE_PICTURE:              
                # remove old profile image
                try:
                    old_picture_path = os.path.join(app.root_path, PATH_PROFILE_PICTURE, current_user.image_file)
                    # remove old picture from file system
                    os.remove(old_picture_path)
                except Exception as e:
                    print(f'Exception: {e}')
                    flash('Something went wrong when updating the profile picture!', 'danger')
                    current_user.image_file = DEFAULT_PROFILE_PICTURE
                    return redirect(url_for('account'))

            # new profile picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
                
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        # it's better to use redirect here
        # so we don't get the message in browser
        # if we want to reload page
        return redirect(url_for('account'))
    # when loading page -> fill form with current data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
