# 新闻详情页模块蓝图
from flask import Blueprint

# 创建蓝图
news_blu = Blueprint("news", __name__, url_prefix="/news")   # 通过 url_prefix 添加前缀

from . import views