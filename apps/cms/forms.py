# cmd/forms.py

from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm
from utils import zlcache
from wtforms import ValidationError
from flask import g

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),
                                    InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='密码长度不够或超出')])
    remember = IntegerField()

class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message="请输入正确格式的旧密码")])
    newpwd = StringField(validators=[Length(6,20,message="请输入正确格式的新密码")])
    newpwd2 = StringField(validators=[EqualTo('newpwd',message="两次输入的密码不一致")])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱")])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确的邮箱验证码')])
    # 自定义验证
    def validate_captcha(self,field):
        #form要提交的验证码和邮箱
        captcha = field.data
        email = self.email.data
        #缓存里面保存的邮箱对应的验证码
        captcha_cache = zlcache.get(email)
        #如果缓存中没有这个验证码，或者缓存中的验证码跟form提交的验证码不相等（不区分大小写）
        # 两个有一个不成立，就抛异常
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误!')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为当前使用的邮箱！')


class AddBannerForm(BaseForm):
    name=StringField(validators=[InputRequired(message='请输入轮播图名称')])
    img_url=StringField(validators=[InputRequired(message='请输入轮播图链接')])
    link_url=StringField(validators=[InputRequired(message='请输入轮播图跳转链接')])
    priority=IntegerField(validators=[InputRequired(message='请输入轮播图优先级')])


class UpdateBannerForm(AddBannerForm):
    banner_id=IntegerField(validators=[InputRequired(message='请输入轮播图ID')])


class AddBoardsForm(BaseForm):
    name=StringField(validators=[InputRequired(message='请输入版块名称'),Length(2,15,message='长度应在2-15个字符之间')])

class UpdateBoardForm(AddBoardsForm):
    board_id=IntegerField(validators=[InputRequired(message='请输入版块名称')])