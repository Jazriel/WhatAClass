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
from itsdangerous import BadSignature
from flask_babel import gettext as _
from sqlalchemy.exc import IntegrityError

from paramiko import SSHClient, AutoAddPolicy
from werkzeug.utils import secure_filename
from os import path

from .forms import LoginForm, SignUpForm, EmailForm, PasswordForm, UploadForm
from .models import User
from .util import email_server, ssh_config
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
    view = 'login.html'

    if current_user.is_authenticated:
        flash(_('There is a logged in user already.'))
        return redirect(url_for('index.base'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if not check_and_login(form.password.data, user):
            return render_template(view, form=form)

        flash(_('Logged in successfully.'))
        return redirect(url_for('index.base'))

    return render_template(view, form=form)


def check_and_login(password, user):
    """Launch exception (that should be used [flask, werkzeug...]) if
    something does not match with what is expected."""
    if user is None or not user.is_correct_password(password):
        flash(_('Email or password were not correct.'))
        return False
    if not user.email_confirmed:
        flash(_('Email was not confirmed yet.'))
        return False
    if not login_user(user):
        flash(_('Something failed, contact your administrator.'))
        return False
    return True


@user_mng.route('/logout')
def logout():
    """Logs the user out, has no effect if there was no one logged in."""
    logout_user()
    return redirect(url_for('index.base'))


@user_mng.route('/signup', methods=['GET', 'POST'])
def sign_up():
    """Creates a user from the email and password given and sends an email with
    a time sensitive serialized url to authenticate the user (ts)."""
    view = 'signup.html'

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
            flash(_('Only one account for each email. (You can use the + tricks.)'))
            return render_template(view, form=form)

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

    return render_template(view, form=form)


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

    view = 'reset.html'

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()

        if not user.email_confirmed:
            flash(_('The email was not confirmed yet.'))
            return render_template(view, form=form)

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
    return render_template(view, form=form)


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


neuralnet_mng = Blueprint('neuralnet_mng', __name__)


@neuralnet_mng.route('/predict', methods=['GET', 'POST'])
# @login_required TODO
def predict():
    """Page where users are going to upload files to get their predictions."""
    form = UploadForm()

    if request.method == 'POST':

        # Standard save file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('neuralnet_mng.fit'))

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('neuralnet_mng.fit'))

        filename = secure_filename(file.filename)
        file.save(path.join('/app/static/images', filename))

        # Start ssh
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(ssh_config['HOST'],
                    port=int(ssh_config['PORT']),
                    username=ssh_config['USER'],
                    key_filename='/root/.ssh/id_rsa')

        _, stdout, stderr = ssh.exec_command(
            'python3 '
            '/scripts/run_inference.py'
            ' {} {} {} {}'.format(path.join('/images', filename),
                                  '/graphs/inceptionv3_model.pb',
                                  '/graphs/inceptionv3_labels.txt',
                                  '/graphs/inceptionv3_label_map_proto.pbtxt'))

        output = stdout.read().decode()

        pairs = output.split(';')
        classes = list()
        probs = list()

        for pair in pairs:
            if pair is not '':
                class_, prob = pair.split(':')
                classes.append(class_)
                probs.append(prob)

        ssh.close()

        if len(classes) < 3 or len(probs) < 3:
            print(output)
            print(stderr.read().decode())
            return render_template('error.html')

        return render_template('fitted.html',
                               classes=classes,
                               probs=probs,
                               image_path=path.join('images', filename))

    return render_template('fit.html', form=form)

