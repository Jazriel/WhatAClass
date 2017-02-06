# -*- coding: utf-8 -*-
"""
    WhatAClass.controllers
    ~~~~~~~~~~~~~~~~~~~~~~

    The usual web-app architecture is the MVC
    (Model-View-Controller). This class implements
    the controllers of the architecture.

    The structure used was Blueprints for the app to
    be scalable (create a divisional or functional
    structure and distribute the work among the contributors).

    :author: Javier Martínez


"""

from flask import (Blueprint, flash, render_template, url_for, abort,
                   redirect, request)
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, SignUpForm, EmailForm, PasswordForm
from itsdangerous import BadSignature
from flask_babel import gettext as _
from sqlalchemy.exc import IntegrityError

from .models import User
from .utils import email_server
from .extensions import db, ts


index = Blueprint('index', __name__)


@index.route('/')
@index.route('/index')
def base():
    """Controller for the index view."""
    return render_template('index.html')


user_mng = Blueprint('user_mng', __name__)


@user_mng.route('/login', methods=['GET', 'POST'])
def login():
    """Try to log in the user with the information provided."""
    if current_user.is_authenticated:
        flash(_('There is a logged in user already.'))
        return redirect(url_for('index.base'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.is_correct_password(form.password.data):
            flash(_('Email or password were not correct.'))
            return redirect(url_for('user_mng.login'))

        if not user.email_confirmed:
            flash(_('Email was not confirmed yet.'))
            return redirect(url_for('user_mng.login'))

        if not login_user(user):
            abort(_('Something failed, contact your administrator.'))
        flash(_('Logged in successfully.'))
        return redirect(url_for('index.base'))

    return render_template('login.html', form=form)


@user_mng.route('/logout')
def logout():
    """Logs the user out, has no effect if there was no one logged in."""
    logout_user()
    return redirect(url_for('index.base'))


@user_mng.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """Creates a user from the email and password given and sends an email with
    a time sensitive serialized url to authenticate the user (ts)."""
    if current_user.is_authenticated:
        flash(_('There is a logged in user already.'))
        return redirect(url_for('index.base'))

    form = SignUpForm()

    if form.validate_on_submit():

        user = User(
            email=form.email.data,
            password=form.password.data
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            return abort(_('Only one account for each email. (You can use the + tricks.)'))

        token = ts.dumps(user.email, salt=b'email-whataclass-salt-key')

        confirm_url = url_for(
            'user_mng.confirm_email',
            token=token,
            _external=True)

        email_body = render_template(
            'email/activate.html',
            confirm_url=confirm_url)

        if not email_server.send_email(user.email,
                                       _('WhatAClass: Confirm your email'),
                                       email_body):
            user.email_confirmed = True
            db.session.add(user)
            db.session.commit()

        flash(_('Signed up successfully.'))

        return redirect(url_for('user_mng.login'))

    return render_template('signup.html', form=form)


@user_mng.route('/confirm/<token>')
def confirm_email(token):
    """Try to see if the token is actually de-cypher-able and try to change
    the user to confirm the email."""
    try:
        email = ts.loads(token, salt=b'email-whataclass-salt-key', max_age=86400)
    except BadSignature:
        return abort(404)

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    flash(_('Email successfully confirmed.'))

    return redirect(url_for('user_mng.login'))


@user_mng.route('/reset', methods=['GET', 'POST'])
def reset():
    """Reset the password given through an email with a time sensitive link."""
    form = EmailForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        if not user.email_confirmed:
            return abort(_('The email was not confirmed yet.'))

        token = ts.dumps(user.email, salt=b'recover-whataclass-key')

        reset_url = url_for(
            'user_mng.recover',
            token=token,
            _external=True)

        body = render_template(
            'email/recover.html',
            reset_url=reset_url)

        if not email_server.send_email(user.email,
                                       _('Password reset requested'),
                                       body):
            flash(_('Feature not available until the '
                    'administrator of the service sets an email.'))

        return redirect(url_for('index.base'))
    return render_template('reset.html', form=form)


@user_mng.route('/recover/<token>', methods=['GET', 'POST'])
def recover(token):
    """Try to get the email from the token and give the chance to change
    password."""
    try:
        email = ts.loads(token, salt=b'recover-whataclass-key', max_age=86400)
    except BadSignature:
        return abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        flash(_('Password successfully changed.'))

        return redirect(url_for('user_mng.login'))

    return render_template('recover.html', form=form, token=token)


file_mng = Blueprint('file_mng', __name__)


@file_mng.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Page where users are going to upload files."""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(_('No file part'))
            return redirect(url_for('file_mng.upload'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash(_('No selected file'))
            return redirect(url_for('file_mng.upload'))
        if file:
            # TODO safe file in db with another model.
            file = file
            return redirect(url_for('file_mng.upload'))
    return render_template('upload.html')


