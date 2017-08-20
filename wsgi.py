# -*- coding: utf-8 -*-
"""
    wsgi
    ~~~~~~~~~~~~~~~~~~~~~~
    Entry point to start the server as 0.0.0.0:80 so that nginx can proxy the traffic.


    :author: Javier Martínez
"""

from WhatAClass.app import create_app_and_db

application = create_app_and_db()

if __name__ == '__main__':
    application.run(host='0.0.0.0', port='80')
