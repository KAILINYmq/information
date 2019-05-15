from flask import session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import app,  db

"""项目入口文件(存放和启动有关的配置)"""
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