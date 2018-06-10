# manage.py
__author__ = 'derek'

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from Perfect_bbs import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel,BoardModel,PostModel

FrontUser = front_models.FrontUser

CMSUser = cms_models.CMSUser

CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

app = create_app()

manager = Manager(app)

Migrate(app,db)   #绑定app跟db
manager.add_command('db',MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    '''创建用户'''
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')

@manager.command
def create_role():
    '''创建角色'''
    # 1.访问者（可以修改个人信息）
    visitor = CMSRole(name='访问者',desc='只能访问数据，不能修改')
    visitor.permissions = CMSPermission.VISITOR

    # 2.运营人员（修改个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营',desc='管理帖子，管理评论，管理前台用户,')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER\
                           |CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER

    # 3.管理员（拥有所有权限）
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER\
                        |CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER

    # 4.开发者
    developer = CMSRole(name='开发者',desc='开发人员专用角色')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.option('-e','--email',dest='email')     #用户邮箱
@manager.option('-n','--name',dest='name')       #角色名字
def add_user_to_role(email,name):
    '''添加用户到某个角色'''
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            #把用户添加到角色里面
            role.users.append(user)
            db.session.commit()
            print("用户添加到角色成功!")
        else:
            print("没有这个角色：%s" %role)
    else:
        print("%s邮箱没有这个用户!"%email)

@manager.command
def test_permission():
    '''测试用户是否有xxx权限'''
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print("这个用户有访问者权限")
    else:
        print("这个用户没有访问者权限")


@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()

@manager.command
def create_test_post():
    for x in range(1,100):
        title='我是标题%s'%x
        content='我是内容,我的编号是%s'%x
        board=BoardModel.query.first()
        author=FrontUser.query.first()
        post=PostModel(title=title,content=content)
        post.board=board
        post.author=author
        db.session.add(post)
        db.session.commit()
    print('测试帖添加成功')


if __name__ == '__main__':
    manager.run()
