from info import constants
from info.models import News, User
from info.modules.news import news_blu
from flask import render_template, current_app, session


@news_blu.route('/<int:news_id>')
def news_detail(news_id):
     """新闻详情"""
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

     data={
         "user": user.to_dict() if user else None,  # 如果user有值执行user.to_dcit() 否则为None
         "news_dict_li": news_dict_li   # 获取主页新闻数据
     }

     return render_template("news/detail.html", data=data)