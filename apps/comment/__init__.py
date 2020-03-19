#!/usr/bin/python3
"""
@Author： deja_ve
@File: __init__.py
@Time: 2020-01-12 18:55
"""
from flask import Blueprint

comment = Blueprint('comment', __name__)

from . import urls
