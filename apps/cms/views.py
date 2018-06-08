# cmd/views.py
__author__ = 'derek'

from flask import Blueprint,views,render_template,request,session,g
from flask import url_for,redirect,jsonify
from .forms import LoginForm,ResetpwdForm,ResetEmailForm
from .models import CMSUser,CMSPermission
from .decorators import login_required,permission_required
import  config
from exts import db,mail
from flask_mail import Message
from utils import restful,zlcache
import string,random

bp = Blueprint("cms",__name__,url_prefix='/cms')

@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))

@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')

@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')

@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')

@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')

@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')

@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


class LoginView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # 31天后过期
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='用户名或密码错误')

        else:
            #form.errors的错误信息格式，是一个字典，value是列表的形式
            # {'email': ['请输入正确的邮箱格式'], 'password': ['密码长度不够或超出']}
            message = form.errors.popitem()[1][0]
            return self.get(message=message)

class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            return restful.params_error(form.get_error())


@bp.route('/email_captcha/')
def email_captcha():
    #获取要修改的邮箱
    email = request.args.get('email')
    if not email:
        return restful.params_error('请输入要修改的邮箱')
    #得到大小写字母的列表
    source = list(string.ascii_letters)
    #得到大小写字母的列表 + 0到9的数字字符串
    source.extend(map(lambda x: str(x), range(0, 10)))
    # 随机取六位作为验证码
    captcha = "".join(random.sample(source, 6))
    #给这个邮箱发送邮件验证码
    message = Message(subject='derek论坛密码修改邮件发送', recipients=[email,], body='你的验证码是：%s'%captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    #把邮箱和验证码保存到memcached中
    zlcache.set(email,captcha)
    return restful.success()

@bp.route('/email/')
def send_email():
    #1.标题，2.收件人，3.发送的正文内容
    message = Message(subject='derek论坛密码修改邮件发送',recipients=['1184405959@qq.com',],body='第一次测试发送邮件')
    mail.send(message)    #发送邮件
    return '邮件发送成功'

class ResetEmail(views.MethodView):
    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'),strict_slashes=False)
bp.add_url_rule('/resetemail/',view_func=ResetEmail.as_view('resetemail'))

