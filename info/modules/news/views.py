from flask.json import jsonify
from info import constants, db
from info.models import News, Comment
from info.modules.news import news_blu
from flask import render_template, current_app, session, g, abort, request
from info.untils.common import user_login_data
from info.untils.response_code import RET

@news_blu.route("/news_comment", methods=["POST"])
@user_login_data
def comment_news():
    """新闻评论"""
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登陆")

    # 1.取到请求参数
    news_id = request.json.get("news_id")
    comment_content = request.json.get("comment")
    parent_id = request.json.get("parent_id")
    # 2.校验参数
    if not all([news_id, comment_content]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    try:
        news_id = int(news_id)
        if parent_id:
            parent_id = int(parent_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 查询新闻，判断是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")
    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到数据")
    # 3.初始化评论模型
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_content
    if parent_id:
        comment.parent_id = parent_id

    # 添加到数据库
    # 自己commit() 因为下面需要用到comment.id
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)

    return jsonify(errno=RET.OK, errmsg="OK", data=comment.to_dict())


@news_blu.route("/news_collect", methods=["POST"])
@user_login_data
def collect_news():
    """收藏新闻"""
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    # 1. 接收参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    # 2. 判断参数
    if not ([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if action not in ["collect", "cancel_collect"]:
        return  jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="参数错误")
    # 3. 查询新闻，判断是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")
    if not news:
        return jsonify(errno=RET.NODATA, errmsg="未查询到数据")

    # 4.收藏和取消收藏
    if action == "cancel_collect":
        # 取消收藏
        if news in user.collection_news:
            # 添加到用户的新闻列表
            user.collection_news.remove(news)
    else:
        if news not in  user.collection_news:
            # 添加到用户的新闻列表
            user.collection_news.append(news)

    return jsonify(errno=RET.OK, errmsg="操作成功")

@news_blu.route('/<int:news_id>')
@user_login_data
def news_detail(news_id):
     """新闻详情"""
     #  1.如果用户登陆，将当前登陆用户的数据传到模板，供模板显示(装饰器方式获取)
     user = g.user

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

     # 查询新闻数据
     news = None
     try:
         news = News.query.get(news_id)
     except Exception as e:
         current_app.logger.error(e)
     if not news:
         # TODO 报404错误后面处理
         abort(404)
     # 更新新闻点击次数
     news.clicks +=1

     # 判断用户是否收藏
     is_collected = False
     if user:
         # 判断用户是否收藏这个新闻
         # 如果当前新闻在用户收藏的新闻里面 user.collection_news后面可以不用加all，因为sqlalchemy会在使用的时候自动加载
         if news in user.collection_news:
             is_collected = True

     data={
         "user": user.to_dict() if user else None,  # 如果user有值执行user.to_dcit() 否则为None
         "news_dict_li": news_dict_li,              # 获取主页新闻数据
         "news": news.to_dict(),                    # 新闻详情页数据
         "is_collected": is_collected               # 判断用户是否收藏
     }

     return render_template("news/detail.html", data=data)