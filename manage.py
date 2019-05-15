from flask_wtf import CSRFProtect
from redis import StrictRedis
from flask import  Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # 可以指定 session 保存的位置
from flask_script import Manager
from flask_migrate import  Migrate,MigrateCommand
from config import Config

"""项目入口文件"""

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