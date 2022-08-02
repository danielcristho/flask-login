from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_required, logout_user, current_user, login, login_fresh

from . import login_manager
from .forms import LoginForm, SignupForm
from .models import User, db
from . import login_manager

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name = form.name.data,
                email = form.email.data,
                website  = form.website.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit() #create new user
            login_user(user) # login as new user
            return redirect(url_for('main_bp.dashboard'))
        flash('A user already exist with that email address')
    return render_template('signup.jinja',
        title = 'Create an Account.',
        form = form,
        template = 'signup-page',
        body = "Sign up for a user account"
    )

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.dashboard'))
        flash('Invalid username or password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template('login.jinja',
        form = form,
        title = 'Log in.',
        template = 'login-page',
        body = "Log in with your User account."
    )

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))