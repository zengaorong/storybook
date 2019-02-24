#coding=utf-8
from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory, \
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import story
from .. import db
from serch import get_serch_list
from app.leotool.bs64pic.pic_to_bs64 import get_picbase64
from ..models import StoryChapter
from .form import fromtest
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 搜索漫画
@story.route('/search', methods=['GET', 'POST'])
def search_story():
    serch_str = "择天记"
    serch_list = get_serch_list(serch_str)
    imagebase64 = get_picbase64("app/leotool/bs64pic/chaotian.jpg")
    return render_template('storybook/story_list.html',serch_list=serch_list,imagebase64=imagebase64)

# 小说内容界面
@story.route('/book/<story>/<chapter>', methods=['GET', 'POST'])
def book(story,chapter):
    storyChapter = StoryChapter.query.filter_by(story_id=story ,chapter_num=chapter).first()
    print  request.user_agent.platform
    # 查询上一章节和下一章节的url
    pre_chapter = db.session.query(StoryChapter.chapter_url).filter(StoryChapter.story_id == story,StoryChapter.chapter_order == storyChapter.chapter_order-1).first()
    lat_chapter = db.session.query(StoryChapter.chapter_url).filter(StoryChapter.story_id == story,StoryChapter.chapter_order == storyChapter.chapter_order+1).first()
    if pre_chapter:
        pre_chapter_url = pre_chapter[0].split('/')[-1].replace('.html',"")
    else:
        pre_chapter_url = ""

    if lat_chapter:
        lat_chapter_url = lat_chapter[0].split('/')[-1].replace('.html',"")
    else:
        lat_chapter_url = ""

    story_text = storyChapter.chapter_text.replace("&amp;1t;/p&gt;","")
    return render_template('storybook/story_base.html',chapter_name=storyChapter.chapter_name,story_data=story_text,pre_chapter_url=pre_chapter_url,lat_chapter_url=lat_chapter_url)

# 小说章节界面
@story.route('/book/<story>', methods=['GET', 'POST'])
def chapter(story):
    # storyChapter = StoryChapter.query.filter_by(story_id=story)
    # print StoryChapter.query.filter_by(story_id=story)
    storyChapter = db.session.query(StoryChapter.chapter_name,StoryChapter.chapter_url).filter(StoryChapter.story_id == story ).order_by(StoryChapter.chapter_order)
    print db.session.query(StoryChapter.chapter_name,StoryChapter.chapter_url).filter(StoryChapter.story_id == story )
    story_chapter_list = []
    for chapter in storyChapter:
        temp_dict = {}
        temp_dict['chapter_name'] = chapter.chapter_name
        temp_dict['chapter_url'] = chapter.chapter_url.replace(".html","")
        story_chapter_list.append(temp_dict)

    #story_text = storyChapter.chapter_text
    return render_template('storybook/story_chapter.html',story_chapter_list=story_chapter_list)


#current_app.config['UPLOADED_PHOTOS_DEST']
import os
def getDate(fileurl):
    loadfile = [fileurl]
    imagedata = []
    while(loadfile):
        try:
            path = loadfile.pop()
            #print path
            for x in os.listdir(path):
                if os.path.isfile(os.path.join(path,x)):
                    imagedata.append(x)
                else:
                    loadfile.append(os.path.join(path,x))


        except Exception,e:
            print str(e) + path

    return imagedata

def getfile(fileurl):
    loadfile = [fileurl]
    imagefile = []
    while(loadfile):
        try:
            path = loadfile.pop()
            for x in os.listdir(path):
                if os.path.isfile(os.path.join(path,x)):
                    pass
                else:
                    loadfile.append(os.path.join(path,x))
                    imagefile.append(x)
        except Exception,e:
            print str(e) + path

    return imagefile

@story.route('/book/piclist', methods=['GET', 'POST'])
def piclist():
    file_url =  getfile(current_app.config['UPLOADED_PHOTOS_DEST'])
    print file_url
    # getDate(getfile(current_app.config['UPLOADED_PHOTOS_DEST'])[0])
    return render_template('storybook/filelist.html',file_url=file_url)

@story.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('storybook/story_index.html')
