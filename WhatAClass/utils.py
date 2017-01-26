# -*- coding: utf-8 -*-
"""
    WhatAClass.utils
    ~~~~~~~~~~~~~~~~

    Utilities for WhatAClass, so that there are no
    functions scattered around.

    :author: Javier Martínez


"""
from itsdangerous import URLSafeTimedSerializer

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

from . import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def send_email(email, subject, body):
    """Send an email to the specified address."""
    # TODO move email address and host,port to the instance/config file
    from_address = 'what.a.class.web@gmail.com'
    msg = MIMEMultipart('alternative')
    msg['From'] = from_address
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    with SMTP(host='smtp.gmail.com', port=587) as server:
        server.ehlo()
        server.starttls()
        password = app.config.get('EMAIL_PASS')
        server.login(from_address, password)
        server.sendmail(from_address, email, msg.as_string())

