#!/usr/bin/python3
"""
@Author： deja_ve
@File: __init__.py
@Time: 2020-01-12 18:02
"""

from flask import Blueprint

user = Blueprint('user', __name__)

from . import urls
# from . import models
