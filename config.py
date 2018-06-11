# config.py
__author__ = 'derek'

import os
# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'abcdefg'
DEBUG = True
DB_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/bbs?charset=utf8"

CMS_USER_ID = 'aaa'    #随便写一值，这样session更加安全
FRONT_USER_ID = 'FFFF'

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

ALIDAYU_APP_KEY = 'LTaAxIWVQxxxxxxT8Q'
ALIDAYU_APP_SECRET = 'AESRSxcqR7e4xxxxcIL8LhJ'
ALIDAYU_SIGN_NAME = '仙剑论坛网站'
ALIDAYU_TEMPLATE_CODE = 'SMS_136870947'

UEDITOR_UPLOAD_PATH=os.path.join(os.path.dirname(__file__),'images')

#分页
PER_PAGE= 10

# celery的配置
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"

