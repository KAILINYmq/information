import time
from datetime import datetime, timedelta
from flask import request, render_template, current_app, session, redirect, url_for, g, abort
from flask.json import jsonify
from info import constants
from info.models import User, News, Category
from info.modules.admin import admin_blu
from info.untils.common import user_login_data
from info.untils.response_code import RET


@admin_blu.route('/news_edit_detail')
def news_edit_detail():
     """新闻版式编辑功能实现"""
     # 1. 获取参数
     news_id = request.args.get("news_id")
     if not news_id:
         abort(404)

     try:
         news_id = int(news_id)
     except Exception as e:
         current_app.logger.error(e)
         return render_template('admin/news_edit_detail.html', errmsg="参数错误")

     try:
         news = News.query.get(news_id)
     except Exception as e:
         current_app.logger.error(e)
         return render_template('admin/news_edit_detail.html', errmsg="查询数据错误")

     if not news:
         return render_template('admin/news_edit_detail.html', errmsg="为查询到数据")

     # 查询分类数据
     categories = []
     try:
         categories = Category.query.all()
     except Exception as e:
         current_app.logger.error(e)
         return render_template('admin/news_edit_detail.html', errmsg="查询数据错误")

     categories_dict_li = []
     for category in categories:
         # TODO 有疑问 取到分类的字典
         cate_dict = category.to_dict()
         # 判断当前遍历的分类是否是当前新闻分类，如果是，添加is_selected为True
         if category.id == news.category_id:
             cate_dict["is_selected"] = True
         categories_dict_li.append(category.to_dict())

     # 移除最新的分类
     categories_dict_li.pop(0)
     data = {
         "news": news.to_dict(),
         "categories":  categories_dict_li
     }

     return render_template('admin/news_edit_detail.html', data=data)


@admin_blu.route('/news_edit')
def news_edit():
    """新闻版式编辑"""
    # 取出参数
    page = request.args.get("p", 1)
    keywords = request.args.get("keywords", None)
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    news_list = []
    current_page = 1
    total_page = 1

    filters = [News.status == 0]
    # 如果关键字存在就添加关键字搜索
    if keywords:
        filters.append(News.title.contains(keywords))
    try:
        paginate = News.query.filter(*filters)\
            .order_by(News.create_time.desc())\
            .paginate(page, constants.ADMIN_NEWS_PAGE_MAX_COUNT, False)
        news_list =paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    news_divt_list = []
    for news in news_list:
        news_divt_list.append(news.to_basic_dict())

    context = {"total_page": total_page,
               "current_page": current_page,
               "news_list": news_divt_list
    }

    return render_template('admin/news_edit.html', data=context)


@admin_blu.route('/news_review_action', methods=["POST"])
def news_review_action():
    """ 添加审核功能"""
    # 1. 接收参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")

    # 2. 校验参数
    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if action not in("accept", "reject"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误" )

    # 3. 查询指定的新闻数据
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.NODATA, errmsg="数据查询失败")

    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到数据")

    if action == "accept":
        # 通过
        news.status = 0
    else:
        # 未通过
        reason = request.json.get("reason")
        if not reason:
            return jsonify(errno=RET.PARAMERR, errmsg="请输入拒绝原因！")
        news.status = -1
        news.reason = reason

    return jsonify(errno=RET.OK, errmsg="OK")


@admin_blu.route('/news_review_detail/<int:news_id>')
def news_review_detail(news_id):
    """添加审核"""
    # 查询数据
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)

    if not news:
        return render_template('admin/news_review_detail.html', data={"errmsg": "为查询到此新闻！"})

    # 返回数据
    data = {"news": news.to_dict()}
    return render_template('admin/news_review_detail.html', data=data)


@admin_blu.route('/news_review')
def review():
    """新闻审核"""
    # 取出参数
    page = request.args.get("p", 1)
    keywords = request.args.get("keywords", None)
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    news_list = []
    current_page = 1
    total_page = 1
    # TODO 有疑问
    filters = [News.status != 0]
    # 如果关键字存在就添加关键字搜索
    if keywords:
        filters.append(News.title.contains(keywords))
    try:
        paginate = News.query.filter(*filters)\
            .order_by(News.create_time.desc())\
            .paginate(page, constants.ADMIN_NEWS_PAGE_MAX_COUNT, False)

        news_list =paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    news_divt_list = []
    for news in news_list:
        news_divt_list.append(news.to_review_dict())

    context = {"total_page": total_page,
               "current_page": current_page,
               "news_list": news_divt_list
    }

    return render_template('admin/news_review.html', data=context)


@admin_blu.route('/user_list')
def user_list():
    """后端用户列表显示"""
    page = request.args.get("page", 1)
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    users_list = []
    current_page = 1
    total_page = 1
    # paginate(p, constants.ADMIN_USER_PAGE_MAX_COUNT) 传入当前第几页 和 渲染多少条数据
    try:
        paginate = User.query.filter(User.is_admin == False).paginate(page, constants.ADMIN_USER_PAGE_MAX_COUNT)
        users_list = paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    users_dict_li = []
    for user in users_list:
        users_dict_li.append(user.to_admin_dict())

    data = {
        "users_dict_li": users_dict_li,
        "current_page": current_page,
        "total_page": total_page
    }

    return render_template('admin/user_list.html', data=data)


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

    # 折线图数据统计
    active_time = []
    active_count = []
    begin_today_date = datetime.strptime(('%d-%02d-%02d' % (t.tm_year, t.tm_mon, t.tm_mday)), "%Y-%m-%d")  # 将时间字符串转化为对象
    for i in range(0, 31):
        begin_date = begin_today_date - timedelta(days=i)     # 取到今天0点
        end_date = begin_today_date - timedelta(days=(i - 1))  # 取到后一天24点
        count = User.query.filter(User.is_admin == False, User.last_login >= begin_date, User.last_login < end_date).count()
        # 活跃人数
        active_count.append(count)
        # 活跃时间
        active_time.append(begin_date.strftime('%Y-%m-%d'))
    # 使数据反转
    active_time.reverse()
    active_count.reverse()

    data = {
        "total_count": total_count,
        "mon_count": mon_count,
        "day_count": day_count,
        "active_time": active_time,
        "active_count": active_count
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
    if not user.check_password(password):
        return render_template('admin/login.html', errmsg="用户名或密码错误")

    # 保存用户信息到session
    session["user_id"] = user.id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name
    session["is_admin"] = user.is_admin

    # 跳转首页
    return redirect(url_for('admin.index'))
