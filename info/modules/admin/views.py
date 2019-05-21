from flask import request, render_template, current_app, session, redirect, url_for
from info.models import User
from info.modules.admin import admin_blu


@admin_blu.route('/index', methods=["GET","POST"])
def index():
    """后台主页"""
    return render_template('admin/index.html')


@admin_blu.route('/login', methods=["GET","POST"])
def login():
    """后台登陆"""
    if request.method =="GET":
        return render_template('admin/login.html')

    # 否则就是登陆
    # 1. 取到登陆参数
    username = request.form.get("username")
    password = request.form.get("password")

    # 2. 验证参数
    if not all([username, password]):
        return render_template('admin/login.html', errmsg="参数错误")

    # 3.查询当前用户
    try:
        user = User.query.filter(User.mobile == username, User.is_admin == True).first()
    except Exception as e:
        current_app.logger.error(e)
        return render_template('admin/login.html', errmsg="用户信息查询失败")
    if not user:
        return render_template('admin/login.html', errmsg="为查询到用户信息")
    # 校验密码
    # TODO 所有登陆存在BUG
    if user.check_password(password):
        return render_template('admin/login.html', errmsg="用户名或密码错误")

    # 保存用户信息到session
    session["user_id"] = user.id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name
    session["is_admin"] = user.is_admin

    # 跳转首页
    return redirect(url_for('admin.index'))
