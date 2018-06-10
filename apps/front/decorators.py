from flask import session,redirect,url_for
from functools import wraps
import config


def login_requried(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if  config.FRONT_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('front.signin'))
    return wrapper