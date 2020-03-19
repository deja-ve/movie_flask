#!/usr/bin/python3
"""
@Author： deja_ve
@File: models.py
@Time: 2020-01-12 18:10
"""
from datetime import datetime

from apps.db.db import db


def get_timestamp():
    timestamp = int(datetime.now().timestamp())
    return timestamp


class Comment(db.Model):
    """
    ID
    movie_id
    user_id
    评论
    添加时间
    """
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号ID
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))  # movie_id
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # user_id
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.Integer, index=True, default=get_timestamp)  # 添加时间

    def __repr__(self):
        return "<Comment> id {}".format(self.id)
