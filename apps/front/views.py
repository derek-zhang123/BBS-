# front/views.py
__author__ = 'derek'

from flask import Blueprint,views,render_template,make_response
from utils.captcha import Captcha
from io import BytesIO

bp = Blueprint("front",__name__)

@bp.route('/')
def index():
    return 'front index'


class SignupView(views.MethodView):
    def get(self):
        return render_template('front/signup.html')

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
