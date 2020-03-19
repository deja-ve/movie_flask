#!/usr/bin/python3
"""
@Author： deja_ve
@File: urls
@Time: 2020-01-12 18:03
"""
from ..user import user

from .views import *

user.add_url_rule('/register', view_func=register, methods=["POST"])
user.add_url_rule('/login', view_func=login, methods=["POST"])
user.add_url_rule('/logout', view_func=logout, methods=["GET"])
user.add_url_rule('/info', view_func=info, methods=["GET", "POST"])
user.add_url_rule('/face', view_func=face, methods=["POST"])
user.add_url_rule('/changPass', view_func=chagnePassword, methods=["POST"])

# from apps import api
# apps.add_url_rule()
# api.add_resource(Login, '/api/login')
# api.add_resource(Register, '/api/register')
# api.add_resource(Info, '/api/info')
