# -*- coding: utf-8 -*-
"""
    WhatAClass.utils
    ~~~~~~~~~~~~~~~~

    Utilities for WhatAClass, so that there are no
    functions scattered around. For now provides
    email functionality.

    :author: Javier Martínez


"""
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP


class EmailServer(object):

    def __init__(self, config=None):
        """Create the EmailServer object, if the config is not specified upon
        initialization, the config property will have to be called.

        :param dict config: This dict should contain:: str FROM, str PASS, str HOST, int PORT
        """
        self._email = None
        self._password = None
        self._host = None
        self._port = None
        if config is not None:
            self.config = config

    def send_email(self, email, subject, body):
        """Send an email to the specified address."""
        msg = MIMEMultipart('alternative')
        msg['From'] = self._email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        with SMTP(host=self._host, port=self._port) as server:
            server.ehlo()
            server.starttls()
            server.login(self._email, self._password)
            server.sendmail(self._email, email, msg.as_string())

    @property
    def config(self):
        """Write-only property that stores the configuration of the email."""
        return None

    @config.setter
    def config(self, cf):
        """Setter of the configuration.

        :param dict cf: This dict should contain:: str FROM, str PASS, str HOST, int PORT"""
        self._email = cf['FROM']
        self._password = cf['PASS']
        self._host = cf['HOST']
        self._port = cf['PORT']


email_server = EmailServer()
