#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:7monthdleo@120.79.217.238/spider'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#story_id story_url,story_name,story_intro,author,story_last_chapter_url,story_last_chapter_name,story_type

class Story(db.Model):
    __tablename__ = 'story'
    story_id = db.Column(db.VARCHAR(36), primary_key=True)
    story_url = db.Column(db.String(64), unique=True)
    story_name = db.Column(db.String(128), unique=True)
    story_intro = db.Column(db.Text())
    author = db.Column(db.String(128))
    story_last_chapter_url = db.Column(db.String(128))
    story_last_chapter_name = db.Column(db.String(128))
    story_type = db.Column(db.Integer)
    image_data = db.Column(db.Text())

    #users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Story %r>' % self.story_name

# 考虑的问题 是否使用ssdb来处理会更好 没有一致性的排序 会使得查询时间非常长 是否隔一段时间 执行排序的操作
#  chapter_id,story_id,chapter_num,chapter_name,chapter_url,chapter_text
class StoryChapter(db.Model):
    __tablename__ = 'storyChapter'
    chapter_id = db.Column(db.VARCHAR(36), primary_key=True)
    story_id = db.Column(db.VARCHAR(36), db.ForeignKey('story.story_id'))
    chapter_num = db.Column(db.Integer)
    chapter_name = db.Column(db.String(128))
    chapter_url = db.Column(db.String(128))
    chapter_text = db.Column(db.Text())

    def __repr__(self):
        return '<StoryChapter %r>' % self.chapter_name



db.create_all()
db.session.commit()