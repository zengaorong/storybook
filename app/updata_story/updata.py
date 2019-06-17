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
import os
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

#url = "http://www.biquge.lu/book/39651/"
# respons = requests.get(url)
# respons.encoding='gbk'
#
# soup = BeautifulSoup(respons.text.replace('\r','\n'),'html.parser')
#
# chapter_soup = soup.find('div',{'class','listmain'})
# chapter_list = chapter_soup.find_all('dd')
# # 除去最新章节的6章
# # chapter_id,story_id,chapter_num,chapter_name,chapter_url,chapter_text
#
# num = 0
# check_num = 5
# for key in chapter_list[6:]:


def get_IP(nums):
    ip_list = []
    for num in range(0,nums):
        url = "http://123.207.35.36:5010/get/"
        respons = requests.get(url)
        ip_list.append(respons.text)
    return ip_list


ip_list = [u'101.251.216.103:8080', u'218.60.8.98:3129', u'61.128.208.94:3128', u'222.74.61.98:53281', u'123.138.89.132:9999']


proxies = {
    'https': 'https://182.61.170.45:3128',
}

url = "http://123.207.35.36:5010/get/"
# url_shuhui = 'http://prod-api.ishuhui.com/ver/ea149533/setting/page?page=/&.json'
# url_biqu = "http://www.biquge.lu/book/16364/"


def __load_one_chapter(chapter_list,key,num):
    check_num = 5
    # print key.string
    chapter_name = key.string
    chapter_url = key.find('a')['href']
    story_id = key.find('a')['href'].split('/')[-2]
    chapter_num = key.find('a')['href'].split('/')[-1].replace('.html',"")
    #http://www.biquge.lu/book/39651/19467857.html
    if check_chapter_todb(story_id,chapter_num) :
        print "have"
        return
    while check_num!=0:
        try:
            story_spider_for_biequge('http://www.biquge.lu/'+key.find('a')['href'],[story_id,chapter_num,chapter_name,chapter_url,chapter_list.index(key)+1])
            num += 1
            print num
            check_num = 0
        except Exception ,e:
            check_num = check_num - 1
            print e
            print chapter_num

    check_num = 5


def getdown_id():
    path_file = "download_id_list.txt"
    download_id_list = []
    if os.path.exists(path_file):
        file = open(path_file,'r')
        for line in file.readlines():
            # 读取文档内容，循环存入漫画id
            download_id_list.append(line.strip().split('\t')[0])

    else:
        file = open(path_file,'w')
        file.close()
    return download_id_list

def dict_to_text(data_dict):
    outstr = ""
    for key in data_dict:
        outstr = outstr + str(data_dict[key][0]) + '\t' + str(data_dict[key][1]) + '\t' + str(data_dict[key][2]) + '\n'
    return outstr

def delete_story_to_text(delete_story_id):
    path_file = "download_id_list.txt"
    download_id_dict = {}
    if os.path.exists(path_file):
        file = open(path_file,'r')
        for line in file.readlines():
            # 读取文档内容，循环存入漫画id
            if line.strip().split('\t')[0] == delete_story_id:
                pass
            else:
                download_id_dict[line.strip().split('\t')[0]] = [line.strip().split('\t')[0],line.strip().split('\t')[1],line.strip().split('\t')[2]]

        file = open("download_id_list.txt",'w')
        file.writelines(dict_to_text(download_id_dict))
        file.close()
    else:
        file = open(path_file,'w')
        file.close()


# for key in getdown_id():
#     print key


for updata_time_id  in getdown_id():
    list = Story.query.filter_by(story_id = updata_time_id)
    num = 0
    s = requests.Session()
    s.keep_alive = False
    for key in list:
        lists = db.session.query(StoryChapter.chapter_name,StoryChapter.chapter_url).filter(StoryChapter.story_id==key.story_id).order_by(StoryChapter.chapter_num).all()
        print len(lists)
        if key.chapter_num==0 or key.chapter_num==None or key.chapter_num=="":
            key.chapter_num = len(lists)
            db.session.add(key)
            db.session.commit()

        url = "http://www.biquge.lu/book/%s/"%key.story_id
        respons = s.get(url)
        respons.encoding='gbk'
        soup = BeautifulSoup(respons.text.replace('\r','\n'),'html.parser')
        chapter_soup = soup.find('div',{'class','listmain'})
        chapter_list = chapter_soup.find_all('dd')
        updata_time = soup.find_all('meta')
        temp_story = key

        check_num = 5
        chapter_list = chapter_list[6:]
        download_threads = []

        chapter_list_indb = db.session.query(StoryChapter.chapter_name,StoryChapter.chapter_num).filter(StoryChapter.story_id==key.story_id).order_by(StoryChapter.chapter_num).all()
        chapter_id_list = []
        chapter_name_list = []
        for key in chapter_list_indb:
            chapter_id_list.append(str(key[1]))
            chapter_name_list.append(str(key[0]))

        wrong_list = []


        for key in chapter_list:
            if key.find('a')['href'].split('/')[-1].replace('.html',"") in chapter_id_list:
                pass
            if key.find('a').string in chapter_name_list:
                pass
            else:
                # wrong_list.append(key.find('a').get_text())
                wrong_list.append(key)


        for key in wrong_list:
            if len(threading.enumerate()) >= 3:
                time.sleep(0.5 + len(threading.enumerate())*0.1)

            download_thread = threading.Thread(target=__load_one_chapter,
                                               args=(chapter_list,key,num))
            download_threads.append(download_thread)
            download_thread.start()
        [ t.join() for t in download_threads ]

    delete_story_to_text(updata_time_id)
    if temp_story.updata_time!= datetime.strptime(updata_time[-3]['content'], "%Y-%m-%d %H:%M:%S") or temp_story.updata_time==0 or temp_story.updata_time==None or key.updata_time=="":
        temp_story.updata_time = datetime.strptime(updata_time[-3]['content'], "%Y-%m-%d %H:%M:%S")
        db.session.add(temp_story)
        db.session.commit()
