#!/usr/bin/python3
"""
@Author： deja_ve
@File: views
@Time: 2020-01-12 18:15
"""
import re
import json
from functools import wraps

from flask import request, json, session, url_for

from .models import Movie, Tag


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


def movie_view():
    """
    :return:
    """
    # _data = request.get_data()
    try:
        data = request.values.to_dict()
    except Exception:
        message = "数据格式有误，请检查数据。"
        return json.dumps({"message": message})
    check_field = ["page"]
    check_flag = all([True for each in check_field if data.get(each, '')])
    if not check_flag:
        message = "数据不完整，请检查数据。"
        return json.dumps({"message": message})
    # 检测数据是否符合要求
    try:
        page = int(re.match(r"\d+", data["page"]).group())
    except Exception:
        message = "数据不合法"
        return json.dumps({"message": message})
    # 每页返回查询数据量
    per_page = 10
    movie_count = Movie.query.count()
    movie_list = Movie.query.order_by(Movie.release_time.desc()).paginate(page, per_page, False).items
    # 此处 当Tag表数据庞大时，该方式将不适用
    tag_list = Tag.query.all()
    tag_dict = {tag.id: tag.name for tag in tag_list}

    if not movie_list:
        message = "无更多数据"
        return json.dumps({"message": message}), 404
    res_list = list()
    for movie in movie_list:
        tag_name = tag_dict.get(movie.tag_id)
        url = url_for("static", filename='uploads/movie/' + movie.url)
        temp = dict({
            "id": movie.id,
            "name": movie.name,
            "brief": movie.brief,
            "tag_name": tag_name,
            "playnum": movie.playnum,
            "commentnum": movie.commentnum,
            "url": url
        })
        res_list.append(temp)

    message = "成功"
    return json.dumps({"count": movie_count, "data": res_list, "message": message}), 200


def detail():
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
    except Exception:
        message = "数据不合法"
        return json.dumps({"message": message})

    movie = Movie.query.filter_by(id=movie_id).first()
    if movie:
        tag = Tag.query.filter_by(id=movie.tag_id).first()
        tag_name = tag.name
        url = url_for("static", filename='uploads/movie/' + movie.url)
        data = dict({
            "id": movie.id,
            "name": movie.name,
            "brief": movie.brief,
            "tag_name": tag_name,
            "playnum": movie.playnum,
            "commentnum": movie.commentnum,
            "release_time": movie.release_time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": url
        })
        message = "成功"
        return json.dumps({"data": data, "message": message}), 200
    else:
        message = "无此电影资源"
        return json.dumps({"data": data, "message": message}), 404
