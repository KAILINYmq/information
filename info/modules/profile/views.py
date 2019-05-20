from flask import render_template, g, redirect, request, jsonify, current_app
from info import constants
from info.modules.profile import profile_blu
from info.untils.common import user_login_data
from info.untils.image_storage import storage
from info.untils.response_code import RET

@profile_blu.route('/pic_info', methods=["GET","POST"])
@user_login_data
def pic_info():
    """用户头像上传"""
    user = g.user
    if request.method == "GET":
        return render_template('news/user_pic_info.html', data={"user": user.to_dict()})

    # 代表用户在保存数据
    # 1. 取到上传的图片
    try:
        avatar = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2.上传头像
    try:
        # 自己封装方法上传
        key = storage(avatar)
    except Exception as e:
        return jsonify(errno=RET.THIRDERR, errmsg="上传头像错误")

    # 3. 保存头像地址到数据库
    user.avatar_url = key
    return jsonify(errno=RET.OK, errmsg="OK", avatar_url=constants.QINIU_DOMIN_PREFIX+key)


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
