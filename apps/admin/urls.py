#!/usr/bin/python3
"""
@Author： deja_ve
@File: urls
@Time: 2020-01-12 18:03
"""
from ..admin import admin

from .views import *

admin.add_url_rule('/register', view_func=register, methods=["POST"])
admin.add_url_rule('/login', view_func=login, methods=["POST"])
admin.add_url_rule('/logout', view_func=logout, methods=["GET"])
admin.add_url_rule('/manage/role', view_func=role, methods=["GET","POST","DELETE"])
admin.add_url_rule('/manage/admin', view_func=admin_view, methods=["GET","POST","DELETE"])
admin.add_url_rule('/manage/user', view_func=user, methods=["GET","POST"])
admin.add_url_rule('/manage/movie', view_func=movie, methods=["GET","POST","DELETE"])
admin.add_url_rule('/manage/tag', view_func=tag, methods=["GET","POST","DELETE"])
admin.add_url_rule('/upload/movie', view_func=upload_movie, methods=["POST"])

# user.add_url_rule('/info', view_func=info, methods=["GET", "POST"])
# user.add_url_rule('/face', view_func=face, methods=["POST"])
# user.add_url_rule('/changPass', view_func=chagnePassword, methods=["POST"])

# from apps import api
# apps.add_url_rule()
# api.add_resource(Login, '/api/login')
# api.add_resource(Register, '/api/register')
# api.add_resource(Info, '/api/info')
