import os
from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from shablog import db, bcrypt
from shablog.models import User, Post
from shablog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from shablog.users.utils import save_picture, send_reset_email
from shablog.config import Constants


users = Blueprint('users', __name__)

# @app -> @users
# @users => look at the name of the Blueprint
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('users.login'))  # redirect to home page
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # if there exist 'next' parameter, then server should
            # redirect to that next page
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # picture is not required
        if form.picture.data:
            # check if default profile picture
            if current_user.image_file != Constants.DEFAULT_PROFILE_PICTURE:              
                # remove old profile image
                try:
                    old_picture_path = os.path.join(current_app.root_path, Constants.PATH_PROFILE_PICTURE, current_user.image_file)
                    # remove old picture from file system
                    os.remove(old_picture_path)
                except Exception as e:
                    print(f'Exception: {e}')
                    flash('Something went wrong when updating the profile picture!', 'danger')
                    # current_user.image_file = Constants.DEFAULT_PROFILE_PICTURE
                    return redirect(url_for('users.account'))

            # new profile picture
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
                
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        # it's better to use redirect here
        # so we don't get the message in browser
        # if we want to reload page
        return redirect(url_for('users.account'))
    # when loading page -> fill form with current data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)  # '\' -> break the line
    return render_template('user_posts.html', posts=posts, user=user)

# send email to be able to reset password
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email with instructions to reset password has been sent!', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Resest Password', form=form)

# here you reset password with token
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    # check if token is valid -> no user was returnedin case of invalid token
    if user is None:
        flash('That is invlid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Resest Password', form=form)

