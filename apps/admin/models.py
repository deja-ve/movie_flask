#!/usr/bin/python3
"""
@Author： deja_ve
@File: models.py
@Time: 2020-03-05 15:52
"""

from apps.db.db import db
from datetime import datetime


class Admin(db.Model):
    """
    管理员
    ID
    名称
    密码(密文储存)
    添加时间
    role_id
    """
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号ID
    nickname = db.Column(db.String(20))  # 网名
    phone = db.Column(db.String(11), unique=True)  # 电话号码
    password = db.Column(db.String(200), unique=True)  # 密码(密文储存)
    sex = db.Column(db.SmallInteger(), default=0)  # 性别

    addtime = db.Column(db.Integer, index=True, default=int(datetime.now().timestamp()))  # 添加时间
    update_time = db.Column(db.Integer, default=int(datetime.now().timestamp()),
                            onupdate=int(datetime.now().timestamp()))  # 修改时间

    # 设置外键
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # role_id

    def __repr__(self):
        return '<Admin id:{}>'.format(self.id)

    def check_pwd(self, pwd):
        """验证密码是否正确"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, pwd)


class AdminLog(db.Model):
    """
    管理员操作日志
    ID
    操作事由
    登录时间
    登录IP
    添加时间
    admin_id
    """
    __tablename__ = "admin_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号ID
    event = db.Column(db.String(100))  # 操作事由
    last_login_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间
    last_ip = db.Column(db.String(50))  # 登录IP
    addtime = db.Column(db.Integer, index=True, default=int(datetime.now().timestamp()))  # 添加时间

    # 设置外键
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # admin_id

    def __repr__(self):
        return '<AdminLog id:{}>'.format(self.id)


class Role(db.Model):
    """
    管理员角色权限等级
    ID
    名称
    权限级别
    添加时间
    修改时间
    """
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号ID
    name = db.Column(db.String(20), unique=True)  # 名称
    level = db.Column(db.Integer)  # 权限级别
    addtime = db.Column(db.Integer, index=True, default=int(datetime.now().timestamp()))  # 添加时间
    update_time = db.Column(db.Integer, default=int(datetime.now().timestamp()),
                            onupdate=int(datetime.now().timestamp()))  # 修改时间

    # 设置外键，关联模型
    admin = db.relationship('Admin', backref='role')  # 收藏外键关系关联

    def __repr__(self):
        return '<Role id:{}>'.format(self.id)