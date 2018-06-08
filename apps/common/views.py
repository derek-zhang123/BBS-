# common/views.py
__author__ = 'derek'

from flask import Blueprint

bp = Blueprint("common",__name__,url_prefix='/common')

@bp.route('/')
def index():
    return 'common index'