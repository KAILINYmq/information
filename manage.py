from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # 可以指定 session 保存的位置
from flask_script import Manager
from flask_migrate import  Migrate,MigrateCommand

"""项目入口文件"""
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


app = Flask(__name__)
# 加载配置
app.config.from_object(Config)

# 初始化数据库
db = SQLAlchemy(app)
# 初始化 redis 存储对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 开启项目 CSRF 保护, 只做服务器验证功能
CSRFProtect(app)
# 设置session保存指定位置
Session(app)

manager = Manager(app)
# 将 app 与db 关联
Migrate(app,db)
# 将迁移命令添加到manager中
manager.add_command('db', MigrateCommand)

@app.route('/')
def index():
    session["name"] = "kailin"
    return "index"

if __name__ == "__main__":
   manager.run()