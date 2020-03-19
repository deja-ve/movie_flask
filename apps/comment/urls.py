#!/usr/bin/python3
"""
@Author： deja_ve
@File: urls
@Time: 2020-01-12 18:03
"""
from . import comment
from .views import *

# comment.add_url_rule('/comment', view_func=comment, methods=["GET", "POST"])

comment.add_url_rule('/', view_func=CommentView.as_view('comment_view'), methods=["POST", "GET"])
# comment.add_url_rule('/login', view_func=comment, methods=["POST"])
