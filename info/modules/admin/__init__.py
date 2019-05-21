from flask import  Blueprint

# 创建蓝图
admin_blu = Blueprint("admin", __name__)

from . import views