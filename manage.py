# encoding:utf-8
from flask import session, current_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app, db, models
from info.models import User

# 项目入口文件(存放和启动有关的配置,不关心具体该如何创建app或者相关逻辑)
# 通过指定的配置名字创建对应配置的app
# create_app方法类似于工厂方法
app = create_app('development')

manager = Manager(app)
# 将 app 与db 关联
Migrate(app,db)
# 将迁移命令添加到manager中
manager.add_command('db', MigrateCommand)


# 添加管理员用户（如：python manage.py createsuperuser -n KIALIN1 -p 123456789）
@manager.option('-n', '-name', dest="name")
@manager.option('-p', '-password', dest="password")
def createsuperuser(name, password):
   if not all([name, password]):
       print("参数不足")
       return None

   user = User()
   user.nick_name = name
   user.mobile = name
   user.password = password
   user.is_admin = True

   try:
      db.session.add(user)
      db.session.commit()
   except Exception as e:
      db.session.rollback()
      print(e)
   print("添加成功!")


if __name__ == "__main__":
   manager.run()
