# -*- coding: utf-8 -*-
"""
Basic script to create the database from the model.
:author: Javier Martínez
"""
from WhatAClass.app import create_app
from WhatAClass.utils import create_all_tables

if __name__ == '__main__':
    application = create_app()
    create_all_tables(app=application)

