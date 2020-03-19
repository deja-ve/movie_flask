#!/usr/bin/python3
"""
@Author： deja_ve
@File: setting
@Time: 2020-02-12 14:49
"""
from redis import Redis
import os

SECRET_KEY = 'asdfghjkl'

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@127.0.0.1/movie"
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 跟踪对象的修改，在本例中用不到调高运行效率，所以设置为False

SESSION_TYPE = 'redis'  # session类型为redis
SESSION_PERMANENT = False  # 如果设置为True，则关闭浏览器session就失效。
# apps.config['SESSION_USE_SIGNER'] = False  # 是否对发送到浏览器上session的cookie值进行加密
SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀
SESSION_REDIS = Redis(  # redis的服务器参数
    host='127.0.0.1',  # 服务器地址
    port=6379)  # 服务器端口
SESSION_COOKIE_HTTPONLY=False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UP_MOVIE_DIR = os.path.join(BASE_DIR, "static/uploads/movie")
UP_FACE_DIR = os.path.join(BASE_DIR, "static/uploads/face")
