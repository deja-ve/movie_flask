#!/usr/bin/python3
"""
@Author： deja_ve
@File: views
@Time: 2020-01-12 18:15
"""
from flask_restful import Resource
from flask import request, json, session, url_for
from werkzeug.security import generate_password_hash
from functools import wraps
from apps.db.db import db
from apps import apps
from .models import User
import re
import os


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
    user = User.query.filter_by(phone=phone).first()
    if user:
        message = "该用户名{}已被使用".format(phone)

    else:
        # 创建新用户账号
        new_user = User(phone=phone,
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
    user = User.query.filter_by(phone=phone).first()
    if user.check_pwd(password):
        session["phone"] = user.phone
        message = "登录成功"
    else:
        message = "账号或密码错误"
    return json.dumps({"message": message})


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


@is_login
def logout():
    session.pop("phone")
    message = "成功"
    return json.dumps({"message": message})


@is_login
def face():
    from uuid import uuid4
    import filetype
    allowed_type = ["jpg", "jepg", "png", "bmp"]
    face_img = request.files.get("file")

    if not face_img:
        message = "文件为空"
        return json.dumps({"message": message}), 406
    # 判断文件类型
    face_type = filetype.guess(face_img).extension
    if face_type not in allowed_type:
        message = "文件格式有误"
        return json.dumps({"message": message}), 406
    # 限制文件大小
    fsize = 0
    block_size = 1024 * 10
    # 文件大小应 <= 2M
    while True:
        chunk = face_img.read(block_size)
        fsize += 1
        if fsize > 200:
            message = "文件过大"
            return json.dumps({"message": message}), 406
        elif not chunk:
            face_img.seek(0, 0)
            break

    face_url = str(uuid4()) + '.' + face_type  # 定义文件名
    face_img.save(os.path.join(apps.config["UP_FACE_DIR"], face_url))  # 保存文件
    user = User.query.filter_by(phone=session["phone"]).first()
    user.face = face_url
    db.session.add(user)
    db.session.commit()
    message = "成功"
    return json.dumps({"message": message})


@is_login
def info():
    if request.method == "GET":
        phone = session.get("phone")
        user = User.query.filter_by(phone=phone).first()

        # 拼装需要返回的数据
        sex = "男" if user.sex=="1" else "女"
        face_url = url_for("static", filename='uploads/face/' + user.face) if user.face else ""
        phone = user.phone if user.phone else ""
        nickname = user.nickname if user.nickname else ""
        info = user.info if user.info else ""
        ret_data = {
            "phone": phone,
            "nickname": nickname,
            "sex": sex,
            "info": info,
            "face": face_url,
        }

        message = "成功"
        return json.dumps({"message": message, "data": ret_data}), 200

    if request.method == "POST":
        _data = request.get_data()
        try:
            data = json.loads(_data)
        except Exception:
            message = "数据格式有误，请检查数据。"
            return json.dumps({"message": message})

        check_field = ['nickname', 'sex', 'info']
        check_flag = all([True for each in check_field if data.get(each, '')])
        if not check_flag:
            message = "数据不完整，请检查数据。"
            return json.dumps({"message": message})

        # 检测数据是否符合要求
        try:
            nickname = re.match(r".{2,20}$", data["nickname"]).group()
            info = re.match(r".{0,200}$", data["info"]).group()
            sex = 1 if re.match(r"[男,女]{1}$", data["sex"]).group() == "男" else 0
        except Exception:
            message = "数据不合法"
            return json.dumps({"message": message})
        phone = session["phone"]
        user = User.query.filter_by(phone=phone).first()
        user.nickname = nickname
        user.info = info
        user.sex = sex
        db.session.add(user)
        db.session.commit()
        message = "成功"
        return json.dumps({"message": message}), 200


@is_login
def chagnePassword():
    _data = request.get_data()
    try:
        data = json.loads(_data)
    except Exception:
        message = "数据格式有误，请检查数据。"
        return json.dumps({"message": message})
    check_field = ["oldPass", 'newPass', 'confirmPass']
    check_flag = all([True for each in check_field if data.get(each, '')])
    if not check_flag:
        message = "数据不完整，请检查数据。"
        return json.dumps({"message": message})

    if data["confirmPass"] != data["newPass"]:
        message = "确认密码错误。"
        return json.dumps({"message": message})

    # 检测数据是否符合要求
    try:
        oldPass = re.match(r".{6,20}", data["oldPass"]).group()
        newPass = re.match(r".{6,20}", data["newPass"]).group()
    except Exception:
        message = "数据不合法"
        return json.dumps({"message": message})

    phone = session.get("phone")
    user = User.query.filter_by(phone=phone).first()
    if user.check_pwd(oldPass):
        user.password = generate_password_hash(newPass)
        db.session.add(user)
        db.session.commit()
        message = "成功"
    else:
        message = "原始密码错误"
    return json.dumps({"message": message}),200
