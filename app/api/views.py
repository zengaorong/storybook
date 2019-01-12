#coding=utf-8

from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory,\
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import api
from .forms import photos
from ..models import Manhua,Chapter
from .. import db
from sqlalchemy import and_
import sys
import uuid
import os


reload(sys)
sys.setdefaultencoding('utf-8')


global mhurl
global mhname
global chaptername

mhurl = []
mhname =''
chaptername = ''

# 测试路径使用
@api.route('/index')
def index():
    print current_app
    print current_app.config['FLASKY_POSTS_PER_PAGE']
    return render_template('mhcontrol/index.html',data='control')


# 漫画名称模糊查询的ajax后台代码 这个可以归属于公共类中 访问者和管理员都能使用
@api.route('/getmhname',methods=['GET', 'POST'])
def getmhname():
    words = [request.args.get('mhname', '', type=str)]
    for w in words:
        print w
    rule = and_(*[Manhua.mhname.like('%' + w + '%') for w in words])
    print rule
    print Manhua.query.filter(rule)
    manhua = Manhua.query.filter(rule)
    chapter_list = []
    for key in manhua:
        chapter_list.append(key.mhname)
    return jsonify(result = chapter_list)


# 后台上传图片的公共类
@api.route('/uploadImage', methods=['POST'])
def flask_upload():

    global mhurl
    global mhname
    global chaptername
    type = request.args.get('type')
    uploadurl = request.args.get('uploadurl')
    mhname = request.args.get('mhname')
    chaptername = request.args.get('chaptername')

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #logger.debug('No file part')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            #logger.debug('No selected file')
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            # try:
            print repr(chaptername)
            print repr(file.filename)

            cwd = os.getcwd()
            filename = photos.save(file,cwd + '/app/static/' + uploadurl + '/' + mhname + '/' + chaptername + '/')
            mhurl.append(mhname + '/' + chaptername + '/' + file.filename )
            return jsonify({'code': 0, 'filename': filename, 'msg': photos.url(filename)})
            # except Exception as e:
            #     #logger.debug('upload file exception: %s' % e)
            #     return jsonify({'code': -1, 'filename': '', 'msg': 'Error occurred'})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


# 后台上传图片的临时存放文件夹
@api.route('/uploadtempImage', methods=['POST'])
def uploadtempImage():

    # global mhurl
    # global mhname
    # global chaptername
    # type = request.args.get('type')
    # uploadurl = 'upload/temp'
    id = request.form.get('id')
    uploadurl = request.form.get('fileurl')
    mhname = request.form.get('manhuaname')
    chaptername = request.form.get('chaptername')

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'code': -1, 'filename': '', 'msg': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'code': -1, 'filename': '', 'msg': 'No selected file'})
        else:
            # try:
            cwd = os.getcwd()
            filename = photos.save(file,cwd + '/app/static/' + uploadurl + '/' + mhname + '/' + chaptername + '/')
            return jsonify({'code': 0, 'filename': mhname + '/' + chaptername + '/' + file.filename, 'msg': photos.url(filename)})
    else:
        return jsonify({'code': -1, 'filename': '', 'msg': 'Method not allowed'})


# 提交数据到数据库中
@api.route('/adddbdata', methods=['POST'])
def add_db_data():
    # print mhurl
    global mhurl
    global mhname
    global chaptername

    data_url = ""
    for key in mhurl:
        data_url = data_url + key + '\n'

    # # 在这里传入
    print mhname
    print chaptername

    mhdata = Manhua.query.filter_by(mhname=mhname).first()
    print mhdata
    print mhdata.id

    chapter = Chapter.query.filter_by(chapter_name=chaptername).first()
    if(chapter==None):
        chapter = Chapter(id=uuid.uuid1(),mhname_id=mhdata.id,data=data_url,chapter_nums=0,pics_nums=len(mhurl),chapter_name=chaptername)
    else:
        chapter.data = data_url

    db.session.add(chapter)
    db.session.commit()

    mhurl = []
    mhname = ''
    chaptername = ''

        # mhdata.mhname = leofrom.mhname.data
        # mhdata.pic_url = leofrom.hidden_pic_url.data
        #
        # db.session.add(mhdata)
        # db.session.commit()


    return jsonify({'code': 'OK'})
# @api.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(current_app.config['UPLOADED_PHOTOS_DEST'],filename)



