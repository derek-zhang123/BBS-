# front/views.py
__author__ = 'derek'

from flask import Blueprint, views, render_template, make_response,request
from flask import session,url_for
from .forms import SignupForm,SigninForm
from utils import restful,safeutils
from .models import FrontUser
from exts import db
import config
from ..models import BannerModel


bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    context = {
        'banners':banners
    }
    return render_template('front/front_index.html',**context)


class SignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/signup.html', return_to=return_to)
        else:
            return render_template('front/signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())



class SigninView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for('front.signup') and safeutils.is_safe_url(
                return_to):
            return render_template('front/signin.html', return_to=return_to)
        else:
            return render_template('front/signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误')
        else:
            return restful.params_error(message=form.get_error())

bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
