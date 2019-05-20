from flask import render_template, g, redirect
from info.modules.profile import profile_blu
from info.untils.common import user_login_data

@profile_blu.route('/info')
@user_login_data
def user_info():
    """个人中心"""
    user = g.user
    if not user:
        # 代表没有登陆重定向到首页
        return redirect('/')

    data = {"user": user.to_dict()

    }

    return render_template('news/user.html', data=data)
