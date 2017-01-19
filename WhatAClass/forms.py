from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField
from wtforms.validators import DataRequired, Email


from .util import get_redirect_target, is_safe_url


class RedirectForm(FlaskForm):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class LoginForm(RedirectForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class SignUpForm(RedirectForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class EmailForm(RedirectForm):
    email = StringField('Email', validators=[DataRequired(), Email()])


class PasswordForm(RedirectForm):
    password = PasswordField('Password', validators=[DataRequired()])

