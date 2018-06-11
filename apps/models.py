from exts import db
from datetime import datetime

class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    img_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('BoardModel', backref='posts')
    author_id = db.Column(db.String(50), db.ForeignKey('front_user.id'), nullable=False)
    author = db.relationship('FrontUser', backref='posts')


class CommentModel(db.Model):
    __tablename__='comment'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    author_id = db.Column(db.String(50), db.ForeignKey('front_user.id'), nullable=False)

    post=db.relationship('PostModel',backref='comments')
    author=db.relationship('FrontUser',backref='comments')


class HighLight(db.Model):
    __tablename__='highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    create_time=db.Column(db.DateTime,default=datetime.now)

    post=db.relationship('PostModel',backref='highlight')