#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:7monthdleo@120.79.217.238/spider'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

'''
id: 百度贴吧的发帖的ID号 
例如6110907830 对应 https://tieba.baidu.com/p/6110907830
name: 帖子名称
url: 帖子url
author: 发帖人
type_flag: 帖子类型 是否置顶 申精 0为普通帖 1为申精 2为置顶 3为置顶申精
type_spider: 0 表示该链接未被爬取过 1 表示该链接无曲谱 2表示该链接有曲谱未爬取 3表示该链接已经爬取
'''
class baidu_tieba(db.Model):
    __tablename__ = 'baidu_tieba'
    id = db.Column(db.VARCHAR(36), primary_key=True)
    name = db.Column(db.String(255))
    tie_url = db.Column(db.String(128))
    author = db.Column(db.String(128))
    type_flag = db.Column(db.String(1))
    type_spider = db.Column(db.String(1))
    def __repr__(self):
        return '<baidu_tieba %r>' % self.name

db.create_all()
db.session.commit()