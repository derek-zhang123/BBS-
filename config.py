# config.py
__author__ = 'derek'

import os
SECRET_KEY = os.urandom(24)

DEBUG = True
DB_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/bbs?charset=utf8"

CMS_USER_ID = 'aaa'    #随便写一值，这样session更加安全

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS =False

# MAIL_USE_TLS 端口号587
# MAIL_USE_SSL 端口号465

MAIL_SERVER = "SMTP.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "1184405959@qq.com"
MAIL_PASSWORD = "zusbbbvfbdyqihag"
MAIL_DEFAULT_SENDER = "1184405959@qq.com"


