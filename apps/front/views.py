# front/views.py
__author__ = 'derek'

from flask import Blueprint, views, render_template, make_response,request
from .forms import SignupForm
from utils import restful,safeutils
from .models import FrontUser
from exts import db

bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    return 'front index'


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


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
