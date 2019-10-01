#coding=utf-8
from flask import render_template, request, \
    current_app,jsonify
from . import story
import sys
import platform
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

header={
    'Content-Type' : 'application/x-www-form-urlencoded',
    'User-Agent' : 'Dalvik/2.1.0 (Linux; U; Android 6.0; EVA-AL10 Build/HUAWEIEVA-AL10)',
}

@story.route('/api/ajaxSearch', methods=['GET', 'POST'])
def ajaxSearch():
    kw = request.form.get('kw')
    cate = request.form.get('cate')
    position = request.form.get('position')
    url = "http://www.shicimingju.com/webApi/ajaxSearch"
    data = {"kw":kw,"cate":cate,"position":position}
    respons = requests.post(url,data=data,headers=header)
    return jsonify(respons.json())


@story.route('/api/itemContent', methods=['GET', 'POST'])
def itemContent():
    scid = request.args.get('scid')
    url = "http://www.shicimingju.com/webApi/itemContent?scid=%s"%scid
    print url
    respons = requests.get(url)
    print respons.text
    return jsonify(respons.json())