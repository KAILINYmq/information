from flask import session, current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db, models

"""项目入口文件(存放和启动有关的配置,不关心具体该如何创建app或者相关逻辑)"""
# 通过指定的配置名字创建对应配置的app
# create_app方法类似于工厂方法
app = create_app('development')

manager = Manager(app)
# 将 app 与db 关联
Migrate(app,db)
# 将迁移命令添加到manager中
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
   manager.run()
