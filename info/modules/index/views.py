from flask import render_template, current_app, session, request
from flask.json import jsonify
from info import constants
from info.models import User, News, Category
from info.untils.response_code import RET
from . import index_blu

@index_blu.route('/news_list')
def news_list():
    """获取首页新闻"""
    # 1. 获取参数
    cid = request.args.get("cid", "1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")

    # 2.检验参数
    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg="新闻查询参数错误！")

    # 3.查询数据
    filters = []
    if cid != 1:  # 查询的不是最新数据
        # 需要添加条件
        filters.append(News.category_id == cid)
    # TODO 有疑问！
    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    # 取到当前页数据
    news_model_list = paginate.items    # 模型对象列表
    total_page = paginate.pages   # 总页数
    current_page = paginate.page  # 当前页数
    # 将模型对象列表转换成字典列表
    news_dict_li = []
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())

    data = {
        "total_page": total_page,
        "current_page": current_page,
        "news_dict_li": news_dict_li
    }

    return jsonify(errno=RET.OK, errmsg="OK", data=data)


@index_blu.route('/')
def index():
    """显示首页"""
    # 1. 如果用户登陆，将当前登陆用户的数据传到模板，供模板显示
    user_id = session.get("user_id", None)
    user = None
    if user_id:
        # 尝试查询用户的模型
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 右侧的新闻排行逻辑
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    # 遍历对象列表，将对象字典添加到字典列表中
    news_dict_li = []
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())

    # 查询分类数据，通过模板的形式渲染出来
    categories = Category.query.all()   # 对象字典
    category_li = []
    for category in categories:
        category_li.append(category.to_dict())

    data = {
        "user": user.to_dict() if user else None,    # 如果user有值执行user.to_dcit() 否则为None
        "news_dict_li": news_dict_li,                # 获取右侧新闻数据
        "category_li": category_li                   # 获取分类数据
    }

    return render_template('news/index.html', data=data)

# 打开网页时，浏览器默认去请求根路径+favicon.ico作为网站标签的小图标
# send_static_file是 flask 去查找指定的静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/xds.ico')