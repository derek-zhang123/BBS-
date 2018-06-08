# cms/models.py
__author__ = 'derek'

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class CMSPermission(object):
    ALL_PERMISSION = 0b11111111
    # 1.访问者的权限
    VISITOR = 0b00000001
    # 2.管理帖子的权限
    POSTER =  0b00000010
    # 3.管理评论的权限
    COMMENTER = 0b00000100
    # 4.管理板块的权限
    BOARDER = 0b00001000
    # 5.管理前台用户的权限
    FRONTUSER = 0b00010000
    # 6.管理后台用户的权限
    CMSUSER = 0b00100000
    # 7.管理后台管理员的权限
    ADMINER = 0b01000000

cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    permissions = db.Column(db.Integer,default=CMSPermission.VISITOR)
    users = db.relationship('CMSUser',secondary=cms_role_user,backref='roles')


class CMSUser(db.Model):
    __tablename__='cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)   #不能为空
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)    #不能重复
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

    @property
    def permissions(self):
        #用户拥有的权限
        if not self.roles:
            return 0
        all_permissions = 0
        #用户所有的角色
        for role in self.roles:
            #取出用户所有角色的所有权限
            permissions = role.permissions
            #把所有权限通过“|=”整合到all_permissions
            all_permissions |= permissions
        return all_permissions

    def has_permission(self,permission):
        # 判断用户是否有‘xxx’权限
        #通过与操作，判断用户是否有‘permission’；得到的结果相等返回true，不相等返回false
        return self.permissions&permission == permission

    @property
    def is_developer(self):
        #判断是不是开发者
        return self.has_permission(CMSPermission.ALL_PERMISSION)

