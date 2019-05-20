# 个人页面相关业务逻辑都放在当前模块中
from flask import Blueprint

# 创建蓝图
profile_blu = Blueprint("profile", __name__, url_prefix="/user")   # 通过 url_prefix 添加前缀

from . import views