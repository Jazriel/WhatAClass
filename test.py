# -*- coding: utf-8 -*-
"""
    test
    ~~~~~~~~~~~~~~~~~~~~~~
    Entry point to start tests.


    :author: Javier Martínez
"""
import pytest


def test_all():
    return pytest.main(['tests/'])

if __name__ == '__main__':
    test_all()

