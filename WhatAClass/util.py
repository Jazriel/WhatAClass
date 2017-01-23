from urllib.parse import urlparse, urljoin
from flask import request
from itsdangerous import URLSafeTimedSerializer

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP

from . import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def send_email(email, subject, body):
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


