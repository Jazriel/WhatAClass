from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from wtforms import StringField, PasswordField
from ..util.safe_redirect import RedirectForm, is_safe_url
from wtforms.validators import DataRequired, Email

user_mng = Blueprint('user_mng', __name__)


class LoginForm(RedirectForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


@user_mng.route('/login', methods=['GET', 'POST'])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        # Login and validate the user.
        # login_user(user)  # TODO User model of the aplication

        flash('Logged in successfully.')

        next_url = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        if not is_safe_url(next_url):
            return abort(400)

        return redirect(next_url or url_for('index.index'))

    return render_template('login.html', form_login=form_login)


class SignUpForm(RedirectForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


@user_mng.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form_sign_up = SignUpForm()
    if form_sign_up.validate_on_submit():
        # Login and validate the user.
        # login_user(user)  # TODO User model of the aplication

        flash('Signed up successfully.')

        next_url = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        if not is_safe_url(next_url):
            return abort(400)

        return redirect(next_url or url_for('index.index'))

    return render_template('signup.html', form_sign_up=form_sign_up)
