import logging
from redis import StrictRedis

class Config(object):
    """项目配置文件"""
    DEBUG = True
    SECRET_KEY = "DvekNWw/tf8R2I9vfdQJx0HvNhCauYb+hiqv/UI6mEEQ8qfRYx96IQDBX65B9OAM"

    # 为数据库添加配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/information?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True   # 如果请求结束时候， 如果指定此配置为True，那么SQLAlchemy会自动执行一次commit

    # Redis的配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # Session保存位置
    SESSION_TYPE = "redis"
    # 开启 session 签名
    SESSION_USE_SIGER = True
    # 指定 Session 保存 redis
    SEESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 设置需要过期
    SESSION_PERMANENT = False
    # 设置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2
    # 设置日志等级
    LOG_LEVEL = logging.DEBUG


class Development(Config):
    """项目配置文件(开发环境下)"""
    DEBUG = True

class ProductionConfig(Config):
    """项目配置文件(生产环境下)"""
    DEBUG = False
    LOG_LEVEL = logging.WARNING

class TestingConfig(Config):
    """项目配置文件(单元测试环境下)"""
    DEBUG = True
    TESTING = True

config = {
    "development": Development,
    "production": ProductionConfig,
    "testing": TestingConfig
}