#!/usr/bin/python3
"""
@Author： deja_ve
@File: models.py
@Time: 2020-01-12 18:10
"""

from apps.db.db import db
from datetime import datetime


class User(db.Model):
    """
    用户
    """
    id = db.Column(db.Integer, primary_key=True)  # 编号ID
    nickname = db.Column(db.String(20))  # 网名
    phone = db.Column(db.String(11), unique=True)  # 电话号码
    password = db.Column(db.String(200), unique=True)  # 密码(密文储存)
    sex = db.Column(db.String(1), nullable=False, default="女")  # 性别
    face = db.Column(db.String(255))  # 头像
    info = db.Column(db.Text)  # 个性简介
    addtime = db.Column(db.Integer, index=True, default=int(datetime.now().timestamp()))  # 添加时间
    update_time = db.Column(db.Integer, default=int(datetime.now().timestamp()),
                            onupdate=int(datetime.now().timestamp()))  # 修改时间

    # 设置外键，关联模型
    userlogs = db.relationship('UserLog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
    secret_protection= db.relationship('SecretProtection', backref='user')  # 评论外键关系关联

    # moviecols = db.relationship('Moviecol', backref='user')  # 收藏外键关系关联

    def __repr__(self):
        return "<User id: {}>".format(self.id)

    def check_pwd(self, pwd):
        """验证密码是否正确"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, pwd)


class UserLog(db.Model):
    """
    会员登录日志
    ID
    user_id
    登录时间
    登录IP
    """
    __tablename__ = "user_log"
    id = db.Column(db.Integer, primary_key=True)  # 编号ID
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    last_login_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间
    addtime = db.Column(db.Integer, index=True, default=int(datetime.now().timestamp()))  # 添加时间

    last_ip = db.Column(db.String(50))  # 登录IP

    def __repr__(self):
        return '<UserLog id:{}>'.format(self.id)




class SecretProtection(db.Model):
    """
    密保（忘记密码时，找回密码时使用）
    ID
    问题
    答案
    用户Id

    """
    __tablename__ = "secret_protection"
    id = db.Column(db.Integer, primary_key=True)  # ID
    question = db.Column(db.String(50), nullable=False)  # 问题
    answer = db.Column(db.String(10), nullable=False)  # 答案
    addtime = db.Column(db.Integer, index=True, default=int(datetime.now().timestamp()))  # 添加时间
    update_time = db.Column(db.Integer, default=int(datetime.now().timestamp()),
                            onupdate=int(datetime.now().timestamp()))  # 修改时间

    # 设置外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # user_id

    def __repr__(self):
        return '<Role id:{}>'.format(self.id)