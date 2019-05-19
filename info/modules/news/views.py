from info import constants
from info.models import News
from info.modules.news import news_blu
from flask import render_template, current_app, session, g, abort
from info.untils.common import user_login_data


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

     data={
         "user": user.to_dict() if user else None,  # 如果user有值执行user.to_dcit() 否则为None
         "news_dict_li": news_dict_li,              # 获取主页新闻数据
         "news": news.to_dict()                    # 新闻详情页数据
     }

     return render_template("news/detail.html", data=data)