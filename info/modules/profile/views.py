from flask import render_template, g, redirect, request
from info.modules.profile import profile_blu
from info.untils.common import user_login_data

@profile_blu.route('/base_info', methods=["GET","POST"])
@user_login_data
def base_info():
    """用户资料显示修改"""
    # 不同的请求方式做不同的事情
    if request.method == "GET":
        user = g.user
        return render_template('news/user_base_info.html', data={"user": user.to_dict()})

    # 代表用户在保存数据


@profile_blu.route('/info')
@user_login_data
def user_info():
    """个人中心"""
    user = g.user
    if not user:
        # 代表没有登陆重定向到首页
        return redirect('/')

    data = {
        "user": user.to_dict()
    }

    return render_template('news/user.html', data=data)
