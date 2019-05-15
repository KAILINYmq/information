from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask
from flask_sqlalchemy import SQLAlchemy

"""项目入口文件"""
class Config(object):
    """项目配置"""
    DEBUG = True

    # 为数据库添加配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/information"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis的配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PASSWORD = "123456"
    REDIS_PORT = 6379

app = Flask(__name__)
# 加载配置
app.config.from_object(Config)

# 初始化数据库
db = SQLAlchemy(app)
# 初始化 redis 存储对象
redis_store = StrictRedis(host=Config.REDIS_HOST, password=Config.REDIS_PASSWORD , port=Config.REDIS_PORT)
# 开启项目 CSRF 保护, 只做服务器验证功能
CSRFProtect(app)

@app.route('/')
def index():
    return "index"

if __name__ == "__main__":
    app.run()