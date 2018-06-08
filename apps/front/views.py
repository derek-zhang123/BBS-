# front/views.py
__author__ = 'derek'

from flask import Blueprint,views,render_template,make_response
from utils.captcha import Captcha
from io import BytesIO

bp = Blueprint("front",__name__)

@bp.route('/')
def index():
    return 'front index'

@bp.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    out = BytesIO()
    image.save(out,'png')   #指定格式为png
    out.seek(0)             #把指针指到开始位置
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


class SignupView(views.MethodView):
    def get(self):
        return render_template('front/signup.html')

bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
