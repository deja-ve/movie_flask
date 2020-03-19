#!/usr/bin/python3
"""
@Author： deja_ve
@File: models.py
@Time: 2020-01-12 18:10
"""

from apps.db.db import db
from datetime import datetime


class Tag(db.Model):
    """
    ID
    名称
    添加时间
    修改时间
    """
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号ID
    name = db.Column(db.String(50), unique=True)
    addtime = db.Column(db.Integer, index=True, default=int(datetime.now().timestamp()))  # 添加时间
    update_time = db.Column(db.Integer, default=int(datetime.now().timestamp()),
                            onupdate=int(datetime.now().timestamp()))  # 修改时间

    movie = db.relationship('Movie', backref='tag')  # 电影外键关系关联

    def __repr__(self):
        return "<Tag> id {}".format(self.id)


class Movie(db.Model):
    """
    ID
    电影名
    简介
    tag_id
    地址(url)
    上映时间
    评分
    播放次数
    添加时间
    修改时间
    """
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号ID
    name = db.Column(db.String(50))  # 电影名
    brief = db.Column(db.Text)  # 简介
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    url = db.Column(db.String(500))  # 地址(url)
    release_time = db.Column(db.Date)  # 上映时间
    score = db.Column(db.SmallInteger)  # 评分
    playnum = db.Column(db.BigInteger)  # 播放次数
    commentnum = db.Column(db.BigInteger)  # 评论量

    addtime = db.Column(db.Integer, index=True, default=int(datetime.now().timestamp()))  # 添加时间
    update_time = db.Column(db.Integer, default=int(datetime.now().timestamp()),
                            onupdate=int(datetime.now().timestamp()))  # 修改时间

    comments = db.relationship("Comment", backref="movie")  # 评论外键关联

    def __repr__(self):
        return "<Movie> id {}".format(self.id)
