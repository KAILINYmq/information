from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask_session import Session  # 可以指定 session 保存的位置
from config import config

"""之后所有模板文件都放info文件夹"""
# 初始化数据库
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config[config_name])
    # 通过app初始化db
    db.init_app(app)
    # 初始化 redis 存储对象
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    # 开启项目 CSRF 保护, 只做服务器验证功能
    CSRFProtect(app)
    # 设置session保存指定位置
    Session(app)

    return  app
