from redis import StrictRedis

class Config(object):
    """项目配置"""
    DEBUG = True
    SECRET_KEY = "DvekNWw/tf8R2I9vfdQJx0HvNhCauYb+hiqv/UI6mEEQ8qfRYx96IQDBX65B9OAM"

    # 为数据库添加配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/information"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
