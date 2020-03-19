#!/usr/bin/python3
"""
@Author： deja_ve
@File: __init__
@Time: 2020-03-05 15:53
"""

from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import urls