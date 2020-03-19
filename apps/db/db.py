#!/usr/bin/python3
"""
@Author： deja_ve
@File: db.py
@Time: 2020-01-12 19:18
"""
import os

from flask_sqlalchemy import SQLAlchemy
from apps import apps

# 创建SQLAlchemy对象
db = SQLAlchemy(apps)
