# common/views.py
__author__ = 'derek'

from flask import Blueprint, request,make_response
from exts import alidayu
from utils import restful, zlcache
from .form import SMSCaptchaForm
from utils.captcha import Captcha
from io import BytesIO

bp = Blueprint("common", __name__, url_prefix='/c')


# @bp.route('/sms_captcha/')
# def sms_captcha():
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请输入手机号码')
#     #生成四位数的验证码
#     captcha = Captcha.gene_text(number=4)
#     if alidayu.send_sms(telephone,code=captcha):
#         return restful.success()
#     else:
#         # return restful.params_error(message='短信验证码发送失败！')
#         return restful.success()
@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    #     telephone+timestamp+salt
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        if alidayu.send_sms(telephone, code=captcha):
            zlcache.set(telephone, captcha)  # 验证码保存到缓存中
            return restful.success()
        else:
            # return restful.paramas_error(message='参数错误')
            zlcache.set(telephone, captcha)  # 测试用
            return restful.success()
    else:
        return restful.params_error(message='参数错误')


@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    zlcache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')   #指定格式为png
    out.seek(0)             #把指针指到开始位置
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp