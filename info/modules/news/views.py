from flask.json import jsonify
from info import constants, db
from info.models import News, Comment, CommentLike
from info.modules.news import news_blu
from flask import render_template, current_app, session, g, abort, request
from info.untils.common import user_login_data
from info.untils.response_code import RET


@news_blu.route('/comment_like', methods=["POST"])
@user_login_data
def comment_like():
    """点赞功能"""
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登陆")
    # 1.取到请求参数
    comment_id = request.json.get("comment_id")
    action = request.json.get("action")
    # 2.校验参数
    if not all([comment_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if action not in ["add", "remove"]:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        comment_id = int(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.PARAMERR, errmsg="参数错误")

    try:
        comment = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    if not comment:
        return jsonify(errno=RET.NODATA, errmsg="评论不存在")

    if action == "add":
        # 点赞评论
        comment_like_model = CommentLike.query.filter(CommentLike.user_id == user.id, CommentLike.comment_id == comment.id).first()
        if not comment_like_model:
            comment_like_model = CommentLike()
            comment_like_model.user_id = user.id
            comment_like_model.comment_id = comment_id
            comment.like_count += 1
            db.session.add(comment_like_model)
    else:
        # 取消点赞
        comment_like_model = CommentLike.query.filter(CommentLike.user_id == user.id, CommentLike.comment_id == comment.id).first()
        if comment_like_model:
            db.session.delete(comment_like_model)
            comment.like_count -= 1
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库操作失败")

    return jsonify(errno=RET.OK, errmsg="OK")


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
     """新闻详情(页面数据初始化)"""
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

     # 查询评论数据
     comments = []
     try:
         # 获取评论通过时间排序
         comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
     except Exception as e:
        current_app.logger.error(e)

     comment_like_ids = []
     if g.user:
         try:
             # 查询用户点赞数据
             # TODO 有疑问
             # 1. 查询当前新闻所有评论 取到所有评论id
             comment_ids = [comment.id for comment in comments]   # 列表推导式
             # 2. 再查询当前评论中哪些被当前用户点赞
             comment_likes = CommentLike.query.filter(CommentLike.comment_id.in_(comment_ids),CommentLike.user_id == g.user.id ).all()
             # 3. 取到所有被点赞的评论id
             comment_like_ids = [comment_like.comment_id for comment_like in comment_likes ]
         except Exception as e:
             current_app.logger.error(e)

     comment_dict_li = []
     for comment in comments:
         comment_dict = comment.to_dict()
         # 初始化点赞
         comment_dict["is_like"] = False
         # 判断当前遍历到的评论是否被当前用户点赞
         if comment.id in comment_like_ids:
             comment_dict["is_like"] = True
         comment_dict_li.append(comment_dict)

     # 新闻详情页用户关注
     is_followed = False
     # if 当前新闻有作者 并且 当前登陆用户已关注过这个用户
     if news.user and user:
         # if user 是否关注过 news.user
         if news.user in user.followers:
             is_followed = True

     data={
         "user": user.to_dict() if user else None,  # 如果user有值执行user.to_dcit() 否则为None
         "news_dict_li": news_dict_li,              # 获取主页新闻数据
         "news": news.to_dict(),                    # 新闻详情页数据
         "is_followed": is_followed,                # 判断用户是否关注
         "is_collected": is_collected,              # 判断用户是否收藏
         "comments": comment_dict_li                # 新闻评论返回
     }

     return render_template("news/detail.html", data=data)