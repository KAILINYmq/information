from flask import render_template, g, redirect, request, jsonify
from info.modules.profile import profile_blu
from info.untils.common import user_login_data
from info.untils.response_code import RET

@profile_blu.route('/pic_info', methods=["GET","POST"])
@user_login_data
def pic_info():
    """用户头像上传"""
    if request.method == "GET":
        user = g.user
        return render_template('news/user_pic_info.html', data={"user": user.to_dict()})



@profile_blu.route('/base_info', methods=["GET","POST"])
@user_login_data
def base_info():
    """用户资料显示修改"""
    # 不同的请求方式做不同的事情
    if request.method == "GET":
        user = g.user
        return render_template('news/user_base_info.html', data={"user": user.to_dict()})

    # 代表用户在保存数据
    # 1. 取到传入参数
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    # 2. 校验参数
    if not all([nick_name, signature, gender]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    if gender not in ("MAN", "WOMAN"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    user = g.user
    user.signature = signature
    user.nick_name = nick_name
    user.gender = gender

    return jsonify(errno=RET.OK, errmsg="OK")




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
