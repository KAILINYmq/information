from flask import render_template, current_app, session
from info.models import User
from . import index_blu

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

    data = {
        "user": user.to_dict() if user else None    # 如果user有值执行user.to_dcit() 否则为None
    }

    return render_template('news/index.html', data=data)

# 打开网页时，浏览器默认去请求根路径+favicon.ico作为网站标签的小图标
# send_static_file是 flask 去查找指定的静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/xds.ico')