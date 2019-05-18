import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from redis import StrictRedis
from flask_session import Session  # 可以指定 session 保存的位置
from config import config
from info.untils.common import do_index_class

"""之后所有模板文件都放info文件夹"""
# 初始化数据库
db = SQLAlchemy()

redis_store = None  # type: StrictRedis

def setup_log(config_name):
    # 创建日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug等级
    # 创建日志记录器， 指明日志保存路径，每个日志文件的最大最小，保护日志文件个数上线
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 *100, backupCount=10)
    # 创建日志记录的格式，日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象 (flask app使用) 添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

def create_app(config_name):
    # 配置日志,并且传入配置名字， 以便能获取到指定配置对应的日志等级
    setup_log(config_name)
    # 创建Flask对象
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])
    # 通过app初始化db
    db.init_app(app)
    # 初始化 redis 存储对象
    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT, decode_responses=True)  # decode_responses=True 设置自动解码
    # 开启项目 CSRF 保护, 只做服务器验证功能
    CSRFProtect(app)
    # 设置session保存指定位置 默认帮我们做了cookie中取出随机值，从表单中取出随机，然后校验，并响应校验结果
    # 我们需要做： 1. 在界面加载时， 往cookie中添加一个csrf_token，2.并且在表单中添加一个隐藏的csrf_token
    Session(app)

    app.add_template_filter(do_index_class, "indexClass")  # 添加自定义过滤器

    # 请求钩子
    @app.after_request
    def after_request(response):
        # 生成随机的csrf_token的值
        csrf_token = generate_csrf()
        # 设置一个cookie
        response.set_cookie("csrf_token", csrf_token)
        return response

    # 注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)
    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)
    from info.modules.news import news_blu
    app.register_blueprint(news_blu)

    return app
