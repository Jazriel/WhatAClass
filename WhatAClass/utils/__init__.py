# -*- coding: utf-8 -*-
"""
    WhatAClass.utils
    ~~~~~~~~~~~~~~~

    Utilities for WhatAClass, so that there are no
    functions scattered around. For now provides
    email functionality.

    :author: Javier Martínez


"""

from .email import EmailServer

from .redirect import is_safe_url


email_server = EmailServer()

ssh_config = dict()


