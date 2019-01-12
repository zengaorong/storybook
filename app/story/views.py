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
    print storyChapter
    story_text = storyChapter.chapter_text
    return render_template('spider/story_base.html',story_data=story_text)

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


