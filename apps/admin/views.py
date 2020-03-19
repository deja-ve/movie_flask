#!/usr/bin/python3
"""
@Author： deja_ve
@File: views
@Time: 2020-01-12 18:15
"""

import re
import os
from functools import wraps

from flask_restful import Resource
from flask import request, json, session, url_for
from werkzeug.security import generate_password_hash

from apps import apps
from apps.db.db import db
from .models import Admin, Role
from apps.user.models import User
from apps.movie.models import Movie, Tag


# 权限要求 装饰器
def auth(rank=None):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            """
            :param rank: 需要权限等级
            :param args:
            :param kwargs:
            :return:
            """
            phone = session.get('phone')
            if not phone:
                message = "请先登录"
                return json.dumps({"message": message}), 401

            admin = Admin.query.filter_by(phone=phone).first()
            role = Role.query.filter_by(id=admin.role_id).first()
            # 判断权限等级
            if role.level >= rank:
                return func(*args, **kwargs)
            message = "权限不足"
            return json.dumps({"message": message}), 401

        return inner

    return decorator


def register():
    """
    用户注册
    """
    _data = request.get_data()
    try:
        data = json.loads(_data)
    except Exception:
        message = "数据格式有误，请检查数据。"
        return json.dumps({"message": message})

    # 检测字段
    check_field = ["phone", 'password', ]
    check_flag = all([True for each in check_field if data.get(each, '')])
    if not check_flag:
        message = "数据不完整，请检查数据。"
        return json.dumps({"message": message})

    # 检测数据是否符合要求
    try:
        phone = re.match(r"1[35678]\d{9}$", data["phone"]).group()
        password = re.match(r".{6,20}", data["password"]).group()
    except Exception:
        message = "数据不合法"
        return json.dumps({"message": message})

    # 检测用户名是否已被使用
    user = Admin.query.filter_by(phone=phone).first()
    if user:
        message = "该用户名{}已被使用".format(phone)

    else:
        # 创建新用户账号
        new_user = Admin(phone=phone,
                         password=generate_password_hash(password),
                         )
        db.session.add(new_user)
        db.session.commit()
        message = "注册成功"
        # return jsonify({"message": message})
    return json.dumps({"message": message})


def login():
    """
    用户登录
    """
    _data = request.get_data()
    try:
        data = json.loads(_data)
    except Exception:
        message = "数据格式有误，请检查数据。"
        return json.dumps({"message": message})
    check_field = ["phone", 'password']
    check_flag = all([True for each in check_field if data.get(each, '')])
    if not check_flag:
        message = "数据不完整，请检查数据。"
        return json.dumps({"message": message})
    # 检测数据是否符合要求
    try:
        phone = re.match(r"1[35678]\d{9}$", data["phone"]).group()
        password = re.match(r".{6,20}", data["password"]).group()
    except Exception:
        message = "数据不合法"
        return json.dumps({"message": message})
    user = Admin.query.filter_by(phone=phone).first()
    if user and user.check_pwd(password):
        session["phone"] = user.phone
        message = "登录成功"
    else:
        message = "账号或密码错误"
    return json.dumps({"message": message})


@auth(rank=1)
def logout():
    session.pop("phone")
    message = "成功"
    return json.dumps({"message": message})


@auth(rank=1)
def role():
    if request.method == "GET":

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
        per_page = 10
        role_list = Role.query.order_by('id').paginate(page, per_page, error_out=False).items
        res_data = list()
        for role in role_list:
            temp = dict({
                "id": role.id,
                "name": role.name,
                "level": role.level,
                "addtime": role.addtime,
                "update_time": role.update_time,
            })
            res_data.append(temp)
        message = "成功"
        return json.dumps({"data": res_data, "message": message}), 200

    if request.method == "POST":
        _data = request.get_data()
        try:
            data = json.loads(_data)
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})
        # 资源修改
        if len(data.keys()) == 3:
            check_field = ["role_id", "name" "level"]
            check_flag = all([True for each in check_field if data.get(each, '')])
            if not check_flag:
                message = "数据不完整，请检查数据。"
                return json.dumps({"message": message})

            # 检测数据是否符合要求
            try:
                role_id = re.match(r"\d+", data["role_id"]).group()
                name = re.match(r".{1,20}", data["name"]).group()
                level = re.match(r"\d+", data["level"]).group()
            except Exception:
                message = "数据不合法"
                return json.dumps({"message": message})

            role = Role.query.filter_by(id=role_id).first()
            role.name = name
            role.level = level
            db.session.add(role)
            db.session.commit()
            message = "成功"
            return json.dumps({"message": message})
        # 资源添加
        if len(data.keys()) == 2:
            check_field = ["name" "level"]
            check_flag = all([True for each in check_field if data.get(each, '')])
            if not check_flag:
                message = "数据不完整，请检查数据。"
                return json.dumps({"message": message})

            # 检测数据是否符合要求
            try:
                # role_id = re.match(r"\d+", data["role_id"]).group()
                name = re.match(r".{1,20}", data["name"]).group()
                level = re.match(r"\d+", data["level"]).group()
            except Exception:
                message = "数据不合法"
                return json.dumps({"message": message})

            new_role = Role(name=name, level=level)
            db.session.add(new_role)
            db.session.commit()
            message = "成功"
            return json.dumps({"message": message})
        else:
            message = "失败"
            return json.dumps({"message": message}), 401

    if request.method == "DELETE":
        try:
            data = request.values.to_dict()
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})

        check_field = ["role_id"]
        check_flag = all([True for each in check_field if data.get(each, '')])
        if not check_flag:
            message = "数据不完整，请检查数据。"
            return json.dumps({"message": message})

        # 检测数据是否符合要求
        try:
            role_id = int(re.match(r"\d+", data["role_id"]).group())
        except Exception:
            message = "数据不合法"
            return json.dumps({"message": message})
        del_role = Role.query.filter_by(id=role_id).first()
        db.session.delete(del_role)
        db.session.commit()
        message = "成功"
        return json.dumps({"message": message}), 200


@auth(rank=1)
def admin_view():
    if request.method == "GET":
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
        per_page = 10
        role_all = Role.query.all()
        role_mapping = dict()
        for role in role_all:
            role_mapping[role.id] = role.name
        admmin_list = Admin.query.order_by('id').paginate(page, per_page, error_out=False).items
        res_data = list()
        for admin in admmin_list:
            temp = dict({
                "id": admin.id,
                "nickname": admin.nickname,
                "phone": admin.phone,
                "addtime": admin.addtime,
                "update_time": admin.update_time,
            })
            temp["sex"] = "女" if admin.sex == 0 else "男"
            temp["role_name"] = role_mapping.get(admin.role_id)
            res_data.append(temp)
        message = "成功"
        return json.dumps({"data": res_data, "message": message}), 200

    if request.method == "POST":
        _data = request.get_data()
        try:
            data = json.loads(_data)
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})
        # 资源修改
        if data.get("admin_id", ''):
            check_field = ["admin_id", "nickname", "phone", "role_name", "sex"]
            check_flag = all([True for each in check_field if data.get(each, '')])
            if not check_flag:
                message = "数据不完整，请检查数据。"
                return json.dumps({"message": message})

            # 检测数据是否符合要求
            try:
                admin_id = re.match(r"\d+", data["admin_id"]).group()
                nickname = re.match(r".{1,20}", data["nickname"]).group()
                phone = re.match(r"1[35678]\d{9}$", data["phone"]).group()
                role_name = re.match(r".{1,20}", data["phone"]).group()
                sex = 1 if re.match(r"[男,女]{1}$", data["sex"]).group() == "男" else 0
            except Exception:
                message = "数据不合法"
                return json.dumps({"message": message})

            admin = Admin.query.filter_by(id=admin_id).first()
            admin.nickname = nickname
            admin.phone = phone
            admin.sex = sex
            admin.role_name = role_name
            db.session.add(admin)
            db.session.commit()
            message = "成功"
            return json.dumps({"message": message})
        # 资源添加
        else:
            check_field = ["nickname", "phone", "role_name", "sex"]
            check_flag = all([True for each in check_field if data.get(each, '')])
            if not check_flag:
                message = "数据不完整，请检查数据。"
                return json.dumps({"message": message})

            # 检测数据是否符合要求
            try:
                nickname = re.match(r".{1,20}", data["nickname"]).group()
                phone = re.match(r"1[35678]\d{9}$", data["phone"]).group()
                role_name = re.match(r".{1,20}", data["role_name"]).group()
                sex = 1 if re.match(r"[男,女]{1}$", data["sex"]).group() == "男" else 0
            except Exception:
                message = "数据不合法"
                return json.dumps({"message": message})
            role = Role.query.filter_by(name=role_name).first()
            new_admin = Admin(nickname=nickname, phone=phone, role_id=role.id, sex=sex)
            new_admin.password = generate_password_hash("123456")
            db.session.add(new_admin)
            db.session.commit()
            message = "成功"
            return json.dumps({"message": message})
        message = "失败"
        return json.dumps({"message": message}), 401

    if request.method == "DELETE":
        try:
            data = request.values.to_dict()
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})

    check_field = ["admin_id"]
    check_flag = all([True for each in check_field if data.get(each, '')])
    if not check_flag:
        message = "数据不完整，请检查数据。"
        return json.dumps({"message": message})

    # 检测数据是否符合要求
    try:
        admin_id = int(re.match(r"\d+", data["admin_id"]).group())
    except Exception:
        message = "数据不合法"
        return json.dumps({"message": message})
    del_admin = Admin.query.filter_by(id=admin_id).first()
    db.session.delete(del_admin)
    db.session.commit()
    message = "成功"
    return json.dumps({"message": message}), 200


@auth(rank=1)
def user():
    # _data = request.get_data()
    try:
        # data = json.loads(_data)
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
    # 每页返回数据
    per_page = 10
    user_list = User.query.order_by('id').paginate(page, per_page, error_out=False).items
    res_data = list()
    sex_mapping = {"0": "女",
                   "1": "男"}
    for user in user_list:
        temp_data = dict({
            "id": user.id,
            "nickname": user.nickname,
            "phone": user.phone,
            "addtime": user.addtime,
            "update_time": user.update_time,
        })
        temp_data["sex"] = sex_mapping.get(user.sex, '')
        res_data.append(temp_data)
    message = "成功"
    return json.dumps({"data": res_data, "message": message}), 200


@auth(rank=1)
def movie():
    if request.method == "GET":
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
        # 每页返回数据
        per_page = 10
        movie_list = Movie.query.order_by('id').paginate(page, per_page, error_out=False).items
        res_data = list()

        for movie in movie_list:
            temp_data = dict({
                "id": movie.id,
                "name": movie.name,
                "brief": movie.brief,
                "score": movie.score,
                "playnum": movie.playnum,
                "commentnum": movie.commentnum,
                "movie_url": movie.url,
                "addtime": movie.addtime,
                "update_time": movie.update_time,
            })
            tag = Tag.query.filter_by(id=movie.tag_id).first()
            temp_data["release_time"] = movie.release_time.strftime("%Y-%m-%d %H:%M:%S")
            temp_data["tag_name"] = tag.name
            res_data.append(temp_data)
        message = "成功"
        return json.dumps({"data": res_data, "message": message}), 200

    if request.method == "POST":
        _data = request.get_data()
        try:
            data = json.loads(_data)
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})

        check_field = ["movie_id", "name", "brief", "tag_name", "release_time", ]
        check_flag = all([True for each in check_field if data.get(each, '')])
        if not check_flag:
            message = "数据不完整，请检查数据。"
            return json.dumps({"message": message})

        # 检测数据是否符合要求
        try:
            movie_id = re.match(r"\d+", data["movie_id"]).group()
            name = re.match(r".{1,50}", data["name"]).group()
            tag_name = re.match(r".{1,20}", data["tag_name"]).group()
            brief = re.match(r".{1,250}", data["brief"]).group()
            release_time = re.match(r".{1,50}", data["release_time"]).group() if data.get(
                "release_time") != 'null' else ''
            score = re.match(r"\d+", data["score"]).group() if data.get("score") != 'null' else ''
            playnum = re.match(r"\d+", data["playnum"]).group() if data.get("playnum") != 'null' else ''
            commentnum = re.match(r"\d+", data["commentnum"]).group() if data.get("commentnum") != 'null' else ''
        except Exception:
            message = "数据不合法"
            return json.dumps({"message": message})
        tag = Tag.query.filter_by(name=tag_name).first()
        movie = Movie.query.filter_by(id=movie_id).first()
        movie.name = name
        movie.brief = brief
        movie.tag_id = tag.id
        if release_time: movie.release_time = release_time
        if score: movie.score = score
        if playnum: movie.playnum = playnum
        if commentnum: movie.commentnum = commentnum

        db.session.add(movie)
        db.session.commit()
        message = "成功"
        return json.dumps({"message": message})

    if request.method == "DELETE":
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
            movie_id = re.match(r"\d+", data["movie_id"]).group()
        except Exception:
            message = "数据不合法"
            return json.dumps({"message": message})
        movie = Movie.query.filter_by(id=movie_id).first()

        db.session.delete(movie)
        db.session.commit()
        message = "成功"
        return json.dumps({"message": message}), 200


@auth(rank=1)
def tag():
    if request.method == "GET":
        tag_items = Tag.query.all()
        res_data = []
        for tag in tag_items:
            temp = {"id": tag.id,
                    "name": tag.name,
                    "addtime": tag.addtime,
                    "update_time": tag.update_time,
                    }
            res_data.append(temp)
        message = "成功"
        return json.dumps({"data": res_data, "message": message})
    if request.method == "POST":

        try:
            _data = request.get_data()
            data = json.loads(_data)
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})

        if len(data.keys()) == 2:
            # 数据校验
            check_field = ["name", "tag_id"]
            check_flag = all([True for each in check_field if data.get(each, '')])
            if not check_flag:
                message = "数据不完整，请检查数据。"
                return json.dumps({"message": message})
            # 检测数据是否符合要求
            try:
                name = re.match(r".{1,50}", data["name"]).group()
                tag_id = re.match(r"\d+", data["tag_id"]).group()
            except Exception:
                message = "数据不合法"
                return json.dumps({"message": message})
            tag = Tag.query.filter_by(id=tag_id).first()
            tag.name = name
            db.session.add(tag)
            db.session.commit()
            message = "成功"
            return json.dumps({"message": message})
        if len(data.keys()) == 1:
            # 数据校验
            check_field = ["name"]
            check_flag = all([True for each in check_field if data.get(each, '')])
            if not check_flag:
                message = "数据不完整，请检查数据。"
                return json.dumps({"message": message})
            # 检测数据是否符合要求
            try:
                name = re.match(r".{1,50}", data["name"]).group()
            except Exception:
                message = "数据不合法"
                return json.dumps({"message": message})
            new_tag = Tag(name=name)
            db.session.add(new_tag)
            db.session.commit()
            message = "成功"
            return json.dumps({"message": message})

    if request.method == "DELETE":
        try:
            data = request.values.to_dict()
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})
        check_field = ["tag_id"]
        check_flag = all([True for each in check_field if data.get(each, '')])
        if not check_flag:
            message = "数据不完整，请检查数据。"
            return json.dumps({"message": message})

        # 检测数据是否符合要求
        try:
            tag_id = re.match(r"\d+", data["tag_id"]).group()
        except Exception:
            message = "数据不合法"
            return json.dumps({"message": message})
        del_tag = Tag.query.filter_by(id=tag_id).first()

        db.session.delete(del_tag)
        db.session.commit()
        message = "成功"
        return json.dumps({"message": message}), 200


def upload_movie():
    # form 表单格式的
    try:
        data = request.values.to_dict()
    except Exception:
        message = "数据格式有误，请检查数据。"
        return json.dumps({"message": message})
    # 数据校验
    check_field = ["name", "brief", "tag_id", "release_time", ]
    check_flag = all([True for each in check_field if data.get(each, '')])
    if not check_flag:
        message = "数据不完整，请检查数据。"
        return json.dumps({"message": message})

    # 检测数据是否符合要求
    try:
        name = re.match(r".{1,50}", data["name"]).group()
        brief = re.match(r".{1,250}", data["brief"]).group()
        tag_id = re.match(r"\d+", data["tag_id"]).group()
        release_time = re.match(r".{1,50}", data["release_time"]).group()
    except Exception:
        message = "数据不合法"
        return json.dumps({"message": message})

    from uuid import uuid4
    allowed_type = ("AVI", "mov", "rmvb", "rm", "FLV", "mp4", "3GP")
    movie_file = request.files.get("file")
    if not movie_file:
        message = "文件为空"
        return json.dumps({"message": message}), 406
    # 判断文件类型
    face_type = movie_file.content_type.split("/")[-1]
    if face_type not in allowed_type:
        message = "文件格式有误"
        return json.dumps({"message": message}), 406
    # 限制文件大小
    fsize = 0
    block_size = 1024 * 100
    # 文件大小应 <= 1G
    while True:
        chunk = movie_file.read(block_size)
        fsize += 1
        if fsize > 10000:
            message = "文件过大"
            return json.dumps({"message": message}), 406
        elif not chunk:
            movie_file.seek(0, 0)
            break
    from datetime import datetime
    release_time = datetime.strptime(release_time, '%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)').strftime('%Y-%m-%d')
    movie_url = str(uuid4()) + '.' + face_type  # 定义文件名
    new_movie = Movie(name=name,
                      brief=brief,
                      tag_id=tag_id,
                      release_time=release_time,
                      url=movie_url
                      )
    db.session.add(new_movie)
    db.session.commit()
    # 数据入库后再保存文件
    movie_file.save(os.path.join(apps.config["UP_MOVIE_DIR"], movie_url))  # 保存文件
    message = "成功"
    return json.dumps({"message": message})
