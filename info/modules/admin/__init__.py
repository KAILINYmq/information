from flask import Blueprint, session, redirect, request, url_for

# 创建蓝图
admin_blu = Blueprint("admin", __name__)

from . import views

xi
# @admin_blu.before_request 表示只在 @admin_blu 的函数里执行
@admin_blu.before_request
def check_admin():
    """如果当前用户不是管理员重定向到主页"""
    is_admin = session.get("is_admin", False)
    if is_admin and request.url.endswith('/admin/login'):
        return redirect('/')