# -*- coding: utf-8 -*-
"""
    WhatAClass.blueprints.index_blue
    ~~~~~~~~~~~~~~~~~~~~~~
    Index blueprint, to add a simple index to the webpage.


    :author: Javier Martínez
"""

from flask import Blueprint, render_template

index = Blueprint('index', __name__)


@index.route('/')
@index.route('/index')
def base():
    """Controller for the index view."""
    return render_template('index.html')