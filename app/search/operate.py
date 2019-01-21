#coding=utf-8
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import  datetime
from data.operatedb import check_story_todb,insert_story_todb
reload(sys)
sys.setdefaultencoding('utf-8')

def get_serch_list(serch_str):
    head = {
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
    }
    url = "http://www.biquge.lu/s.php?ie=gbk&s=15244670192641769733&q=%s"%serch_str
    respons = requests.get(url,headers=head)
    soup = BeautifulSoup(respons.text.replace('\r','\n'),"html.parser")
    div_lists = soup.find_all("div",{'class','bookbox'})

    story_list = []
    for cell in div_lists:
        temp_list = []
        #print type(cell)
        list_a = cell.find_all('a')
        story_url,story_last_chapter_url,story_name,story_last_chapter_name = list_a[1]['href'],list_a[2]['href'],list_a[1].string,list_a[2].string
        author = cell.find('div',{'class','author'}).string
        img_url = cell.find('div',{'class','bookimg'}).contents[0].contents[0]['src']
        story_intro = cell.find('p').string
        story_id =  story_url.split('/')[-2]
        temp_dict = {
            'story_id' : story_id,
            'story_url' : story_url,
            'img_url' : img_url,
            'story_name' : story_name,
            'story_intro' : story_intro,
            'author' : author,
            'story_last_chapter_url' : story_last_chapter_url.replace('.html',''),
            'story_last_chapter_name' : story_last_chapter_name
        }
        story_list.append(temp_dict)
        if not check_story_todb(story_id):
            print story_name
            insert_story_todb([story_id , story_url,story_name,story_intro,author,story_last_chapter_url,story_last_chapter_name,0])

    return story_list
