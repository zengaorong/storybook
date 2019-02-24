#coding=utf-8
from flask import render_template, redirect, request, url_for, flash,jsonify,send_from_directory, \
    current_app
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import search
from .. import db
from operate import get_serch_list,check_story_todb
from app.leotool.bs64pic.pic_to_bs64 import get_picbase64
from ..models import StoryChapter,Story
import sys




from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import time
from bs4 import BeautifulSoup
from data.operatedb import check_chapter_todb ,insert_story_todb
from storys import story_spider_for_biequge

reload(sys)
sys.setdefaultencoding('utf-8')

head = {
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
}



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

def add_story(story_id):
    # list = Story.query.filter_by()
    # print list
    # for key in list:
    #     print key
    list = Story.query.filter_by()
    num = 0
    s = requests.Session()
    for key in list:
        lists = db.session.query(StoryChapter.chapter_name,StoryChapter.chapter_url).filter(StoryChapter.story_id==key.story_id).order_by(StoryChapter.chapter_num).all()
        print len(lists)


        if key.chapter_num==0 or key.chapter_num==None or key.chapter_num=="":
            key.chapter_num = len(lists)
            db.session.add(key)
            db.session.commit()

        url = "http://www.biquge.lu/book/%s/"%key.story_id
        # respons = requests.get(url, proxies={
        #     'https': ip_list[num%5],
        # })

        respons = s.get(url)


        respons.encoding='gbk'

        soup = BeautifulSoup(respons.text.replace('\r','\n'),'html.parser')

        chapter_soup = soup.find('div',{'class','listmain'})
        chapter_list = chapter_soup.find_all('dd')

        check_num = 5
        chapter_list = chapter_list[6:]
        for key in chapter_list[len(lists):]:
            print key.string
            chapter_name = key.string
            chapter_url = key.find('a')['href']
            story_id = key.find('a')['href'].split('/')[-2]
            chapter_num = key.find('a')['href'].split('/')[-1].replace('.html',"")
            #http://www.biquge.lu/book/39651/19467857.html
            print [story_id,chapter_num,chapter_name,chapter_url,chapter_list.index(key)+1]
            if check_chapter_todb(story_id,chapter_num) :
                print "have"
                continue
            while check_num!=0:
                try:
                    story_spider_for_biequge('http://www.biquge.lu/'+key.find('a')['href'],[story_id,chapter_num,chapter_name,chapter_url,chapter_list.index(key)+1])
                    num += 1
                    print num
                    check_num = 0
                except Exception ,e:
                    check_num = check_num - 1
                    print "error"
                    print repr(e)

            check_num = 5


# 搜索漫画
@search.route('/', methods=['GET', 'POST'])
def search_story():
    stname = request.args.get('stname',"",str)
    serch_str = stname
    serch_list = get_serch_list(serch_str)
    #imagebase64 = get_picbase64("app/leotool/bs64pic/chaotian.jpg")
    return render_template('storybook/story_list.html',serch_list=serch_list)

# 添加小说进数据库测试
@search.route('/addstory', methods=['GET', 'POST'])
def addstory():

    stid = request.form.get('stid',"",str)
    print stid
    if check_story_todb(stid):
        pass
    else:
        return jsonify(data="ok")




