#coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

import json

'''
posts 为各个楼层 posts 是一个数组 类型是
'''

class LouCen(object):
    def __init__(self,num,author,datatime,text):
        self.num = num
        self.author = author
        self.datatime = datatime
        self.text = text


class Tieba(object):
    def __init__(self,author,title,url,posts):
        self.author = author
        self.title = title
        self.url = url
        self.posts = posts

def object_tieba_tojson(obj):
    return {

    }


# loucen = LouCen(1,"leo","2019-04-11 23:44","check check check")
# print json.dumps(loucen.__dict__)
# tieba = Tieba("leo","bilibili","http://www.baidu.com",[loucen])
# print json.dumps(tieba.__dict__)