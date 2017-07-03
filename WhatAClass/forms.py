# -*- coding: utf-8 -*-
"""
    WhatAClass.forms
    ~~~~~~~~~~~~~~~~

    Forms used by the controller to get input from the user.

    :author: Javier Martínez


"""
from flask_wtf.file import FileField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email



class UploadForm(FlaskForm):
    """Form used to upload files."""
    file = FileField(u'File', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Login form which is composed of email and password. uses the same
    fields as signup form but in case both diverge they have been
    duplicated."""
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    password = PasswordField(u'Password', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    """Sign up form which is composed of email and password. uses the same
    fields as signup form but in case both diverge they have been
    duplicated."""
    email = StringField(u'Email', validators=[DataRequired(), Email()])
    password = PasswordField(u'Password', validators=[DataRequired()])


class EmailForm(FlaskForm):
    """Email form with only an email address required."""
    email = StringField(u'Email', validators=[DataRequired(), Email()])


class PasswordForm(FlaskForm):
    """Password form with only a password required."""
    password = PasswordField(u'Password', validators=[DataRequired()])


class SelectDatasetForm(FlaskForm):
    """Select form consists of just one select field for a dataset."""
    choice = SelectField(u'Dataset')



