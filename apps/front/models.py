# front/models.py
__author__ = 'derek'

import shortuuid
import enum
from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4

class FrontUser(db.Model):
    __tablename__ = "front_user"
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    gender = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,*args,**kwargs):
        #如果传入的参数里面有‘password’，就单独处理
        if "password" in kwargs:
            self.password = kwargs.get("password")
            #处理完后把password pop出去
            kwargs.pop("password")
            #剩下的参数交给父类去处理
        super(FrontUser, self).__init__(*args,**kwargs)

    @property
    def password(self):
        return self._password

    #保存密码的时候加密
    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result




