#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import time
from bs4 import BeautifulSoup
from data.operatedb import check_chapter_todb
from storys import story_spider_for_biequge
from datetime import datetime
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:7monthdleo@120.79.217.238/story'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


head = {
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
}

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
    chapter_num = db.Column(db.Integer)
    image_data = db.Column(db.Text())
    updata_time = db.Column(db.DATETIME)

    def __repr__(self):
        return '<Story %r>' % self.story_name

class Story_for_update(db.Model):
    __tablename__ = 'Story_for_update'
    story_id = db.Column(db.VARCHAR(36), primary_key=True)
    story_name = db.Column(db.String(128), unique=True)
    author = db.Column(db.String(128))
    updata_time = db.Column(db.DATETIME)

    #users = db.relationship('User', backref='role', lazy='dynamic')
    def __repr__(self):
        return '<Story_for_update %r>' % self.story_id


class StoryChapter(db.Model):
    __tablename__ = 'storyChapter'
    chapter_id = db.Column(db.VARCHAR(36), primary_key=True)
    story_id = db.Column(db.VARCHAR(36), db.ForeignKey('story.story_id'))
    chapter_num = db.Column(db.Integer)
    chapter_name = db.Column(db.String(128))
    chapter_url = db.Column(db.String(128))
    chapter_text = db.Column(db.Text())
    chapter_order = db.Column(db.Integer)

    def __repr__(self):
        return '<StoryChapter %r>' % self.chapter_name


def dict_to_text(data_dict):
    outstr = ""
    for key in data_dict:
        outstr = outstr + str(data_dict[key][0]) + '\t' + str(data_dict[key][1]) + '\t' + str(data_dict[key][2]) + '\n'
    return outstr

list = Story.query.filter_by()
s = requests.Session()
s.keep_alive = False
updata_time_id_dict = {}
for key in list:
    url = "http://www.biquge.lu/book/%s/"%key.story_id
    respons = s.get(url)
    respons.encoding='gbk'
    soup = BeautifulSoup(respons.text.replace('\r','\n'),'html.parser')
    chapter_soup = soup.find('div',{'class','listmain'})
    chapter_list = chapter_soup.find_all('dd')
    updata_time = soup.find_all('meta')

    if key.updata_time!= datetime.strptime(updata_time[-3]['content'], "%Y-%m-%d %H:%M:%S") or key.updata_time==0 or key.updata_time==None or key.updata_time=="":
        updata_time_id_dict[key.story_id] = [key.story_id,key.story_name,key.author]



file = open("download_id_list.txt",'w')
file.writelines(dict_to_text(updata_time_id_dict))
file.close()