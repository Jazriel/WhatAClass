from flask import Blueprint, request, session, redirect, url_for

from WhatAClass.extensions import oauths

oauth_google = Blueprint('oauth_google', __name__, url_prefix='/google')

google_ = oauths['google']


@oauth_google.route('/login')
def login():
    return google_.authorize(callback=url_for('authorized', _external=True))


@oauth_google.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@oauth_google.route('/login/authorized')
def authorized():
    resp = google_.authorized_response()
    if resp is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    # me = google_.get('userinfo')
    return redirect(url_for('index'))

