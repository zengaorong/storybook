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

# 漫画首页
@story.route('/leotest', methods=['GET', 'POST'])
def index():
    return render_template('spider/loading.html')

# 搜索漫画
@story.route('/search/story', methods=['GET', 'POST'])
def search_story():
    serch_str = "元尊"
    serch_list = get_serch_list(serch_str)
    imagebase64 = get_picbase64("app/leotool/bs64pic/chaotian.jpg")
    return render_template('spider/story_list.html',serch_list=serch_list,imagebase64=imagebase64)

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
    return render_template('spider/story_base.html',chapter_name=storyChapter.chapter_name,story_data=story_text,pre_chapter_url=pre_chapter_url,lat_chapter_url=lat_chapter_url)

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
    return render_template('spider/story_chapter.html',story_chapter_list=story_chapter_list)


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
                    imagefile.append(x.decode("gbk"))
        except Exception,e:
            print str(e) + path

    return imagefile

@story.route('/book/piclist', methods=['GET', 'POST'])
def piclist():
    file_url =  getfile(current_app.config['UPLOADED_PHOTOS_DEST'])
    # getDate(getfile(current_app.config['UPLOADED_PHOTOS_DEST'])[0])
    return render_template('spider/filelist.html',file_url=file_url)

@story.route('/pics/<pic>', methods=['GET', 'POST'])
def pic(pic):
    image_list = getDate(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],pic))
    print pic
    print image_list[0]
    return render_template('spider/test.html',pic=pic,image_list=image_list)


ALLOWED_EXTENSIONS = ['jpg', 'png']

def allowe_file(filename):
    '''
    限制上传的文件格式
    :param filename:
    :return:
    '''
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@story.route('/upload', methods=['GET', 'POST'])
def updata():
    return render_template('spider/upload.html')



import os
from werkzeug.utils import secure_filename
import uuid
@story.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # file = request.files.get('文件名') # 获取文件
    filelist = request.files.getlist("fileFolder")
    for file in filelist:
        filename = secure_filename(file.filename)  # 获取文件名
        mkdir(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],file.filename.split('/')[0]))
        print os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],file.filename.split('/')[0])
        file.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], file.filename)) # 保存文件
    excel_dict = {}
    return "ok"


def mkdir(path):

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    print path
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        #print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        #print path+' 目录已存在'
        return False