from datetime import datetime
import random
import re
from flask import request, abort, current_app, make_response, session
from flask.json import jsonify
from info import redis_store, constants, db
from info.libs.yuntongxun.sms import CCP
from info.models import User
from info.untils.response_code import RET
from . import passport_blu
from info.untils.captcha.captcha import captcha

@passport_blu.route('/login', methods=["POST"])
def login():
    """登陆"""
    # 1.获取参数
    params_dict = request.json
    mobile = params_dict.get("mobile")
    passport = params_dict.get("passport")

    #  2.校验参数
    if not all([mobile, passport]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")
    # 校验手机号
    if not re.match('1[]35678]\\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机格式正确")

    #  3.校验密码是否正确
    # 判断是否有手机号
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误！")
    # 查询用户是否存在
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在！")

    # 校验当前密码手否一致
    if not user.check_password(passport):
        return jsonify(errno=RET.PWDERR, errmsg="用户名或密码错误！")

    #  4.保存用户状态
    session["user_id"] = user.id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name

    #  5.响应
    return jsonify(errno=RET.OK, errmsg="登录成功")


@passport_blu.route('/register', methods=["POST"])
def register():
    """注册逻辑"""
    # 1. 获取参数
    param_dict = request.json
    mobile = param_dict.get("mobile")
    smscode = param_dict.get("smscode")
    password = param_dict.get("password")

    # 2. 校验参数
    if not all([mobile, smscode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误！")
    # 校验手机号
    if not re.match('1[]35678]\\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机格式正确")

    # 3. 取到服务器保存的真实的短信验证码
    try:
        real_sms_code = redis_store.get("SMS_" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return  jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    if not real_sms_code:
        return  jsonify(errno=RET.NODATA, errmsg="验证码已过期")

    # 4. 校验用户输入的短信验证码内容和真实验证码的内容是否一致
    if real_sms_code != smscode:
        return  jsonify(errno=RET.DATAERR, errmsg="验证码输入错误")

    # 5. 如果一致, 初始化User模型 并且赋值属性
    user = User()
    user.mobile = mobile
    user.nick_name = mobile  # 暂时没有昵称用手机号代替
    user.last_login = datetime.now()  # 记录最后一次登录时间
    # TODO 对密码处理

    #  6. 将 User 模型添加到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    # 7. 往 session 中保存数据表示当前已经登陆
    session["user_id"] = user.id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name

    # 8. 返回响应
    return jsonify(errno=RET.OK, errmsg="注册成功")

@passport_blu.route('/sms_code',methods=['POST'])
def send_sms_code():
    """发送短信逻辑"""
    # 1. 获取参数: 手机号， 图片验证码内容， 图片验证码的编号（随机值）
    # params_dict = json.loads(request.data)
    params_dict = request.json
    mobile = params_dict.get("mobile")
    image_code = params_dict.get("image_code")
    image_code_id = params_dict.get("image_code_id")

    # 2. 校验参数（参数是否符合规则，判断是否有值）
    # 验证是否有值
    if not all([mobile, image_code, image_code_id]):
        # {"errno":"4100", "errmsg": "参数有误"}
        return jsonify(errno = RET.PARAMERR, errmsg="参数有误")
    # 验证手机号是否正确
    if not re.match('1[35678]\\d{9}', mobile):
        return jsonify(errno = RET.PARAMERR, errmsg="手机号有误")

    # 3. 先从 redis 中取出真实的验证码内容
    try:
        real_image_code = redis_store.get("ImageCodeId_" + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="图片验证码已过期")

    # 4. 与用户的验证码内容进行对比，如果对比不一致，那么返回验证码输入错误
    if real_image_code.upper() != image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="验证码输入错误")

    # 5. 如果一致，生成验证码的内容（随机数据）
    # 随机数字， 保证6位不够会自动在前面补0
    sms_code_str = "%06d" % random.randint(0, 999999)
    current_app.logger.debug("短信验证码是:%s" % sms_code_str)

    # 6. 发送短信验证码
    result = CCP().send_template_sms('15737961721', [sms_code_str, constants.SMS_CODE_REDIS_EXPIRES/60], 1)
    if result != 0:
        return jsonify(error=RET.THIRDERR, errmsg="短信发送失败")

    # 7.验证码保存到 redis
    try:
        redis_store.set("SMS_" + mobile, sms_code_str, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg="数据保存失败")

    # 8. 告知发送结果
    return jsonify(error=RET.OK, errmsg="发送成功")


@passport_blu.route('/image_code')
def get_image_code():
    """生成图片验证码"""
    # 1.取到参数
    # args: 取到url中 ? 后面的参数
    image_code_id = request.args.get("imageCodeId", None)

    # 2.判断参数是否有值
    if not image_code_id:
        return abort(403)

    # 3.生成图片验证码
    name, text, image = captcha.generate_captcha()

    # 4.保存图片验证码文字内容到redis
    try:
        redis_store.set("ImageCodeId_" + image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    # 5.返回验证码图片
    responese = make_response(image)
    # 设置数据类型, 以便浏览器更加智能识别是什么类型
    responese.headers["Content-Type"] = "image/jpg"
    return responese