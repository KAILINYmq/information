# 共用的自 定义工具类
# 过滤器
import functools
from flask import session, current_app, g
from info.models import User

def do_index_class(index):
    """返回指定索引对应的类名"""
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"
    return ""

def user_login_data(news_detail):
    """装饰器获取用户是否登陆"""
    # 使用@functools.wraps去装饰内层函数，可以防止当前装饰器修改内层函数__name__的值不变
    @functools.wraps(news_detail)
    def wrapper(*args, **kwargs):

        # 1. 如果用户登陆，将当前登陆用户的数据传到模板，供模板显示
        user_id = session.get("user_id", None)
        user = None
        if user_id:
            # 尝试查询用户的模型
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        # 查询出来的数据赋值给g变量
        g.user = user

        return news_detail(*args, **kwargs)
    return wrapper