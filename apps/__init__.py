#!/usr/bin/python3
"""
@Author： deja_ve
@File: __init__.py
@Time: 2020-01-12 18:17
"""

from flask import Flask
from flask_session import Session

# from redis import Redis
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

apps = Flask(__name__, static_folder='../static', static_url_path='/static')
apps.config.from_object("apps.config.setting")
Session(apps)

from .user import user
from .admin import admin
from .movie import movie
from .comment import comment

# 功能（app）注册
apps.register_blueprint(user, url_prefix='/user')
apps.register_blueprint(admin, url_prefix='/admin')
apps.register_blueprint(movie,url_prefix='/movie')
apps.register_blueprint(comment, url_prefix='/comment')

# models声明,使得flask-migrate组件可以读取到
from .user.models import *
from .admin.models import *
from .movie.models import *
from .comment.models import *
