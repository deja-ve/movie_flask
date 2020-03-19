#!/usr/bin/python3
"""
@Author： deja_ve
@File: urls
@Time: 2020-01-12 18:03
"""
from ..movie import movie

from .views import *

movie.add_url_rule('/', view_func=movie_view, methods=["GET"])
movie.add_url_rule('/detail', view_func=detail, methods=["GET"])