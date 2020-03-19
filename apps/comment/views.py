#!/usr/bin/python3
"""
@Author： deja_ve
@File: views
@Time: 2020-01-12 18:15
"""
from functools import wraps
import re

from flask import request, json, session, views

from apps.db.db import db
from apps import apps
from .models import Comment
from apps.user.models import User
from apps.movie.models import Movie


def is_login(func):
    """
    装饰器：验证用户是否登录
    :param func:
    :return:
    """

    @wraps(func)
    def inner(*args, **kwargs):
        if not getattr(func, 'is_login', True):
            return func(*args, **kwargs)
        user = session.get('phone')
        if user:
            return func(*args, **kwargs)
        message = "请先登录"
        return json.dumps({"message": message}), 401

    return inner


# def comment():
#     if request.method == "GET":
#         try:
#             data = request.values.to_dict()
#         except Exception:
#             message = "数据格式有误，请检查数据。"
#             return json.dumps({"message": message})
#         check_field = ["movie_id"]
#         check_flag = all([True for each in check_field if data.get(each, '')])
#         if not check_flag:
#             message = "数据不完整，请检查数据。"
#             return json.dumps({"message": message})
#
#         # 检测数据是否符合要求
#         try:
#             movie_id = int(re.match(r"\d+", data["movie_id"]).group())
#             if data.get("page"):
#                 page = int(re.match(r"\d+", data["page"]).group())
#             else:
#                 page = 1
#         except Exception:
#             message = "数据不合法"
#             return json.dumps({"message": message})
#         per_page = 10
#         comment_count = Comment.query.count()
#         comment_list = Comment.query.filter_by(movie_id=movie_id
#                                                ).order_by(Comment.addtime.desc()
#                                                           ).paginate(page, per_page, error_out=False).items
#         res_list = list()
#         for comment in comment_list:
#             user= User.query.filter_by(id=comment.user_id).first()
#             temp = dict({"comment_id": comment.id,
#                          "movie_id": comment.movie_id,
#                          "content": comment.content,
#                          "user_name": user.nickname,
#                          "addtime": comment.addtime
#                          })
#             res_list.append(temp)
#         message = "成功"
#         return json.dumps({"count": comment_count, "data": res_list, "message": message})




class CommentView(views.View):

    def dispatch_request(self):
        if request.method == "POST":
            return self.post()
        if request.method == "GET":
            return self.get()

    def get(self):
        try:
            data = request.values.to_dict()
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})
        check_field = ["movie_id"]
        check_flag = all([True for each in check_field if data.get(each, '')])
        if not check_flag:
            message = "数据不完整，请检查数据。"
            return json.dumps({"message": message})

        # 检测数据是否符合要求
        try:
            movie_id = int(re.match(r"\d+", data["movie_id"]).group())
            if data.get("page"):
                page = int(re.match(r"\d+", data["page"]).group())
            else:
                page = 1
        except Exception:
            message = "数据不合法"
            return json.dumps({"message": message})
        per_page = 10
        comment_count = Comment.query.count()
        comment_list = Comment.query.filter_by(movie_id=movie_id
                                               ).order_by(Comment.addtime.desc()
                                                          ).paginate(page, per_page, error_out=False).items
        res_list = list()
        for comment in comment_list:
            user = User.query.filter_by(id=comment.user_id).first()
            temp = dict({"comment_id": comment.id,
                         "movie_id": comment.movie_id,
                         "content": comment.content,
                         "user_name": user.nickname,
                         "addtime": comment.addtime
                         })
            res_list.append(temp)
        message = "成功"
        return json.dumps({"count": comment_count, "data": res_list, "message": message})

    @is_login
    def post(self):
        try:
            _data = request.get_data()
            data = json.loads(_data)
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})
        check_field = ["movie_id", "content"]
        check_flag = all([True for each in check_field if data.get(each, '')])
        if not check_flag:
            message = "数据不完整，请检查数据。"
            return json.dumps({"message": message})

        # 检测数据是否符合要求
        try:
            movie_id = int(re.match(r"\d+", data["movie_id"]).group())
            content = re.match(r".{1,200}", data["content"]).group()
        except Exception:
            message = "数据不合法"
            return json.dumps({"message": message})
        phone = session.get('phone')
        if not Movie.query.filter_by(id=movie_id).first():
            message = "该电影资源不存在了"
            return json.dumps({"message": message})

        user_id = User.query.filter_by(phone=phone).first().id
        new_comment = Comment(
            movie_id=movie_id,
            content=content,
            user_id=user_id
        )

        db.session.add(new_comment)
        db.session.commit()
        message = "成功"
        return json.dumps({"message": message}), 200
