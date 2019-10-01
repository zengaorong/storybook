
#coding=utf-8
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import  datetime
from data.operatedb import insert_story_todb,check_story_todb
reload(sys)
sys.setdefaultencoding('utf-8')

# head = {
#     "Connection": "keep-alive",
#     "Cache-Control": "no-cache",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
#     "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
# }




url = "https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=4"
respons = requests.get(url,timeout=30)
soup = BeautifulSoup(respons.text,"html.parser")
storys_page_list = soup.find_all("div",{"class":"book-mid-info"})

temp_session = requests.session()
for key in storys_page_list:
    actor_name = key.find("a",{"class":"name"})
    story_name = key.find("a",{"target":"_blank"})
    biqu_url = "http://www.biquge.lu/s.php?ie=gbk&s=15244670192641769733&q=%s"%story_name
    print biqu_url
    break
    respons = temp_session.get(biqu_url)
    soup = BeautifulSoup(respons.text,"html.parser")
    # print soup
    div_list = soup.find_all("div",{'class','bookbox'})
    #print div_list

    # 小说库 小说id 小说url 最近章节url 章节名称 最新章节url 名称 作者 简介
    # 对于数据库 添加章节字段 但是不是在该处 而是执行更新的时候
    #(story_id story_url,story_name,story_intro,author,story_last_chapter_url,story_last_chapter_name,story_type

    story_list = []
    for cell in div_list:
        temp_list = []
        #print type(cell)
        list_a = cell.find_all('a')
        story_url,story_last_chapter_url,story_name_search,story_last_chapter_name = list_a[1]['href'],list_a[2]['href'],list_a[1].string,list_a[2].string
        #print story_url,story_chapter_url,story_name,story_chapter_name
        author = cell.find('div',{'class','author'}).string
        story_intro = cell.find('p').string
        # print story_url,story_last_chapter_url,story_name,story_last_chapter_name,author,story_intro
        story_id =  story_url.split('/')[-2]
        if author.replace("作者：","") == actor_name.string:
            if check_story_todb(story_id):
                pass
            else:
                print author
                insert_story_todb([story_id , story_url,story_name_search,story_intro,author,story_last_chapter_url,story_last_chapter_name,0])


