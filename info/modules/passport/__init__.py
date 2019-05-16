# 登陆注册相关业务逻辑都放在当前模块中
from flask import Blueprint

# 创建蓝图
passport_blu = Blueprint("passport", __name__, url_prefix="/passport")   # 通过 url_prefix 添加前缀

from . import views