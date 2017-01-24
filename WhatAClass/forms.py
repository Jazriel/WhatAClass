# -*- coding: utf-8 -*-
"""
    WhatAClass.forms
    ~~~~~

    Forms used by the controller to get input from the user.


"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    """Login form which is composed of email and password. uses the same
    fields as signup form but in case both diverge they have been
    duplicated."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    """Sign up form which is composed of email and password. uses the same
    fields as signup form but in case both diverge they have been
    duplicated."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class EmailForm(FlaskForm):
    """Email form with only an email address required."""
    email = StringField('Email', validators=[DataRequired(), Email()])


class PasswordForm(FlaskForm):
    """Password form with only a password required."""
    password = PasswordField('Password', validators=[DataRequired()])

