from flask import render_template, current_app
from info import redis_store
from . import index_blu

@index_blu.route('/')
def index():
    return  render_template('news/index.html')

# 打开网页时，浏览器默认去请求根路径+favicon.ico作为网站标签的小图标
# send_static_file是 flask 去查找指定的静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/xds.ico')