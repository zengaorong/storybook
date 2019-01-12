#coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
from storys import story_spider_for_biequge
from data.operatedb import check_chapter_todb
reload(sys)
sys.setdefaultencoding('utf-8')

def getchapter(url):

    #url = "http://www.biquge.lu/book/39651/"
    respons = requests.get(url)
    respons.encoding='gbk'

    soup = BeautifulSoup(respons.text.replace('\r','\n'),'html.parser')

    chapter_soup = soup.find('div',{'class','listmain'})
    chapter_list = chapter_soup.find_all('dd')
    # 除去最新章节的6章
    # chapter_id,story_id,chapter_num,chapter_name,chapter_url,chapter_text

    num = 0
    check_num = 5
    for key in chapter_list[6:]:
        chapter_name = key.string
        chapter_url = key.find('a')['href']
        story_id = key.find('a')['href'].split('/')[-2]
        chapter_num = key.find('a')['href'].split('/')[-1].replace('.html',"")
        #http://www.biquge.lu/book/39651/19467857.html
        if check_chapter_todb(story_id,chapter_num) :
            print "have"
            continue
        while check_num!=0:
            try:
                story_spider_for_biequge('http://www.biquge.lu/'+key.find('a')['href'],[story_id,chapter_num,chapter_name,chapter_url])
                num += 1
                print num
                check_num = 0
            except:
                check_num = check_num - 1
                print "error"
                print chapter_num

        check_num = 5