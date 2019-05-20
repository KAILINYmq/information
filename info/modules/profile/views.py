from flask import render_template, g, redirect, request, jsonify, current_app
from info import constants, db
from info.models import Category, News
from info.modules.profile import profile_blu
from info.untils.common import user_login_data
from info.untils.image_storage import storage
from info.untils.response_code import RET


@profile_blu.route('/pass_info', methods=["GET", "POST"])
@user_login_data
def pass_info():
    """修改密码模板"""
    # 显示界面
    if request.method == "GET":
        return render_template('news/user_pass_info.html')

    # 提交数据（修改密码）
    # 1.获取参数
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")
    # 2.检验参数
    if not all([old_password, new_password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 3.校验旧密码
    user = g.user
    if not user.check_password(old_password):
        return jsonify(errno=RET.PWDERR, errmsg="原密码错误")

    # 4.设置新密码
    user.password = new_password

    return jsonify(erno=RET.OK, errmsg="保存成功")



@profile_blu.route('/news_list')
@user_login_data
def user_news_list():
    """新闻发布审核列表"""
    # 1.获取参数
    page = request.args.get("p", 1)
    # 2.参数判断
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    user = g.user
    news_list = []
    current_page = 1
    total_page =1
    try:
        paginate = News.query.filter(News.user_id == user.id).paginate(page, constants.USER_COLLECTION_MAX_NEWS, False)
        news_list = paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    news_dict_li = []
    for news in news_list:
        news_dict_li.append(news.to_review_dict())

    data = {
        "news_list": news_dict_li,
        "total_page": total_page,
        "current_page": current_page
    }

    return render_template('news/user_news_list.html', data=data)


@profile_blu.route('/news_release', methods=["GET", "POST"])
@user_login_data
def news_release():
    """新闻发布模块"""
    if request.method == "GET":
        # 1. 加载新闻分类数据
        categories = []
        try:
            categories = Category.query.all()
        except Exception as e:
            current_app.logger.error(e)

        categories_dict_li = []
        for category in categories:
            categories_dict_li.append(category.to_dict())
        # 删除为  最新 分类的数据
        categories_dict_li.pop(0)
        return render_template('news/user_news_release.html', data={"categories": categories_dict_li})

    # 2.发布新闻（获取要提交的数据）
    title = request.form.get("title")
    source = '个人发布'
    digest = request.form.get('digest')
    content = request.form.get('content')
    index_image = request.files.get('index_image')
    category_id = request.form.get('category_id')
    # 2.1判断数据是否有值
    if not all([title, source, digest, content, index_image, category_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数有误")
    # 2.2
    try:
        category_id = int(category_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数有误")

    # 3. 将图片上传到云
    try:
        index_image_data = index_image.read()
        key = storage(index_image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    news = News()
    news.title = title
    news.digest = digest
    news.source = source
    news.content = content
    news.index_image_url = constants.QINIU_DOMIN_PREFIX + key
    news.category_id = category_id
    news.user_id = g.user.id
    # 1代表审核状态
    news.status = 1

    try:
        db.session.add(news)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    return jsonify(errno=RET.OK, errmsg="OK")


@profile_blu.route('/pic_info', methods=["GET","POST"])
@user_login_data
def pic_info():
    """用户头像上传"""
    user = g.user
    if request.method == "GET":
        return render_template('news/user_pic_info.html', data={"user": user.to_dict()})

    # 代表用户在保存数据
    # 1. 取到上传的图片
    try:
        avatar = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2.上传头像
    try:
        # 自己封装方法上传
        key = storage(avatar)
    except Exception as e:
        return jsonify(errno=RET.THIRDERR, errmsg="上传头像错误")

    # 3. 保存头像地址到数据库
    user.avatar_url = key
    return jsonify(errno=RET.OK, errmsg="OK", data={"avatar_url": constants.QINIU_DOMIN_PREFIX+key})


@profile_blu.route('/base_info', methods=["GET","POST"])
@user_login_data
def base_info():
    """用户资料显示修改"""
    # 不同的请求方式做不同的事情
    if request.method == "GET":
        user = g.user
        return render_template('news/user_base_info.html', data={"user": user.to_dict()})

    # 代表用户在保存数据
    # 1. 取到传入参数
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 2. 校验参数
    if not all([nick_name, signature, gender]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if gender not in ("MAN", "WOMAN"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    user = g.user
    user.signature = signature
    user.nick_name = nick_name
    user.gender = gender

    return jsonify(errno=RET.OK, errmsg="OK")




@profile_blu.route('/info')
@user_login_data
def user_info():
    """个人中心"""
    user = g.user
    if not user:
        # 代表没有登陆重定向到首页
        return redirect('/')

    data = {
        "user": user.to_dict()
    }

    return render_template('news/user.html', data=data)
