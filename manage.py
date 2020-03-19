#!/usr/bin/python3
"""
@Author： deja_ve
@File: manager.py
@Time: 2020-01-12 18:16
"""

# from flask import Flask
#
# app = Flask(__name__)

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from apps import apps
from apps.db.db import db

db.init_app(apps)

# apps.config['DEBUG'] = True

manager = Manager(apps)
migrate = Migrate(apps, db)

# 添加 db 命令，并与 MigrateCommand 绑定
manager.add_command('db', MigrateCommand)


# manager.add_command('apps', MigrateCommand)

if __name__ == '__main__':
    # app.run()
    manager.add_command("runserver", Server(use_debugger=True))
    manager.run()
