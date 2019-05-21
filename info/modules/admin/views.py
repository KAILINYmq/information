import time
from datetime import datetime
from flask import request, render_template, current_app, session, redirect, url_for, g
from info.models import User
from info.modules.admin import admin_blu
from info.untils.common import user_login_data

@admin_blu.route('/user_count')
def user_count():
    """后台页面数据显示"""
    # 获取数据 总人数
    total_count = 0
    try:
        total_count = User.query.filter(User.is_admin == False).count()
    except Exception as e:
        current_app.logger.error(e)

    # 获取数据 月新增数
    mon_count = 0
    t = time.localtime()  # 获取当前时间
    begin_mon = datetime.strptime(('%d-%02d-01' % (t.tm_year, t.tm_mon)), "%Y-%m-%d")  # 将时间字符串转化为对象
    try:
        mon_count = User.query.filter(User.is_admin == False, User.create_time > begin_mon).count()
    except Exception as e:
        current_app.logger.error(e)

    # 获取数据 日新增数
    day_count = 0
    begin_day = datetime.strptime(('%d-%02d-%02d' % (t.tm_year, t.tm_mon, t.tm_mday)), "%Y-%m-%d")  # 将时间字符串转化为对象
    try:
        day_count = User.query.filter(User.is_admin == False, User.create_time > begin_day).count()
    except Exception as e:
        current_app.logger.error(e)

    data = {
        "total_count": total_count,
        "mon_count": mon_count,
        "day_count": day_count,
    }

    return render_template('admin/user_count.html', data = data)


@admin_blu.route('/index', methods=["GET","POST"])
@user_login_data
def index():
    """后台主页"""
    user = g.user
    return render_template('admin/index.html', data = user.to_dict())


@admin_blu.route('/login', methods=["GET","POST"])
def login():
    """后台登陆"""
    if request.method == "GET":
        # 判断当前用户是否登陆 如果登陆直接重定向到管理员界面
        user_id = session.get("user_id", None)
        is_admin = session.get("user_id", False)
        if user_id and is_admin:
            return redirect(url_for('admin.index'))

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
