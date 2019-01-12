
#coding=utf-8
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import  datetime
from data.operatedb import insert_story_todb,update_chapter_todb,check_chaptertext_isnull
reload(sys)
sys.setdefaultencoding('utf-8')

head = {
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
}

chaptertext_list = check_chaptertext_isnull()
num = len(chaptertext_list)
try_num = 5

# url = "http://www.biquge.lu/book/16364/14551807.html"
# respons = requests.get(url,headers=head)
# soup = BeautifulSoup(respons.text.replace('\r','\n'),"html.parser")
# div_list = soup.find("div" ,id="content")
# print div_list

for key in chaptertext_list:
    while try_num!=0:
        respons = requests.get('http://www.biquge.lu/' + key[4],headers=head)
        soup = BeautifulSoup(respons.text.replace('\r','\n'),"html.parser")
        div_list = soup.find("div" ,id="content")
        if div_list == None:
            try_num = try_num - 1
            if try_num == 0:
                print "wrong story url is:%s"%key[4]
            time.sleep(0.5)
            continue
        else:
            update_chapter_todb(div_list,key[1],key[2])
            if num%10==1:
                print num
            num = num -1
            try_num = 5

            break
    try_num = 5