#coding=utf-8
from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory, \
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import search
from .. import db
from operate import get_serch_list
from app.leotool.bs64pic.pic_to_bs64 import get_picbase64
from ..models import StoryChapter
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 搜索漫画
@search.route('/story', methods=['GET', 'POST'])
def search_story():
    serch_str = "元尊"
    serch_list = get_serch_list(serch_str)
    imagebase64 = get_picbase64("app/leotool/bs64pic/chaotian.jpg")
    return render_template('spider/story_list.html',serch_list=serch_list,imagebase64=imagebase64)




