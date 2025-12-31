# /Splity_flask/Splity/authentication/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from Splity.forms.forms import LoginForm, RegistrationForm
from Splity.services import authentication_services

authentication_blueprint = Blueprint("authentication", __name__)

@authentication_blueprint.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            authentication_services.add_user_service(name=form.name.data,
                                             username=form.username.data,
                                             email=form.email.data,
                                             password=form.password.data)
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('authentication.login'))
        except authentication_services.AuthenticationException as e:
            flash(str(e), 'danger')
    return render_template('authentication/register.html', form=form)


@authentication_blueprint.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = authentication_services.authenticate_user_service(username=form.username.data,
                                                             password=form.password.data)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home.home'))
        except authentication_services.AuthenticationException:
            flash('Invalid username or password', 'danger')
    return render_template('authentication/authentication.html', form=form)


@authentication_blueprint.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home.home'))