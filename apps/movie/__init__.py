#!/usr/bin/python3
"""
@Author： deja_ve
@File: __init__.py
@Time: 2020-01-12 18:02
"""
from flask import Blueprint

movie = Blueprint('movie', __name__)

from . import urls
