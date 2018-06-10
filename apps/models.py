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