#coding=utf-8
import sys
import time
import uuid
import requests
from bs4 import BeautifulSoup
from datetime import  datetime
from data.operatedb import insert_chapter_todb
reload(sys)
sys.setdefaultencoding('utf-8')

head = {
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
}

# ip_list = [u'101.251.216.103:8080', u'218.60.8.98:3129', u'61.128.208.94:3128', u'222.74.61.98:53281', u'123.138.89.132:9999']
# respons = requests.get(url, proxies={
#     'https': ip_list[num%5],
# })

res_session = requests.session()

def story_spider_for_biequge(url,list):
    respons = res_session.get(url,headers=head,timeout=30)
    # with open("result.html","w") as f:
    #     f.writelines(respons.text.replace('\r','\n'))
    #
    soup = BeautifulSoup(respons.text.replace('\r','\n'),"html.parser")
    div_list = soup.find("div" ,id="content")
    insert_chapter_todb([uuid.uuid1(),list[0],list[1],list[2],list[3],div_list,list[4]])








# lists = []
# with open("result1.html","r") as f:
#     lists = f.readlines()
#
# for key in lists:
#     print repr(key)
#     print key
#
# print '<!DOCTYPE html>\r<html>\r<body id="wrapper">\r</body>\r</html>'