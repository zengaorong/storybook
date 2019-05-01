#coding=utf-8
import requests
import sys
import json
from datetime import datetime
from bs4 import BeautifulSoup
from operatedb import insert_baidu_tieba_todb,checks_tieba_todb
reload(sys)
sys.setdefaultencoding('utf-8')

# 获取百度贴吧某个贴吧的全部帖子url
tieba_session= requests.session()
def get_page_datas(index_url):
    respons = tieba_session.get(index_url)
    soup = BeautifulSoup(respons.text,"html.parser")
    # 这里可以吐槽下百度的代码格式
    end_page_url = soup.find('a',{"class","last pagination-item "})['href']
    return int(end_page_url.split('=')[-1])/50 + 1


origin_url = "https://tieba.baidu.com/f?kw=justice_eternal&ie=utf-8"

if __name__ == "__main__":
    page_nums = get_page_datas(origin_url)
    for page in range(0,page_nums):
        print page
        page_url = "https://tieba.baidu.com/f?kw=justice_eternal&ie=utf-8&pn=%s"%str(page*50)
        respons = tieba_session.get(page_url)
        soup = BeautifulSoup(respons.text,"html.parser")
        tiezhi_list = soup.find_all('div',{'class':'threadlist_lz clearfix'})

        page_list = []
        for tiezhi in tiezhi_list:
            try:
                id = tiezhi.find('a',{'class':'j_th_tit '})['href'].split('/')[-1]
                name = repr(tiezhi.find('a',{'class':'j_th_tit '})['title'])
                tie_url = "https://tieba.baidu.com/p/%s"%id
                if tiezhi.find('span',{'class':'tb_icon_author '}):
                    author = repr(tiezhi.find('span',{'class':'tb_icon_author '})['title'].replace("主题作者: ",""))
                else:
                    author = repr(tiezhi.find('span',{'class':'tb_icon_author no_icon_author'})['title'].replace("主题作者: ",""))
                top_num = 2 if tiezhi.find('i',{'class':'icon-top'})  else 0
                good_num = i = 1 if tiezhi.find('i',{'class':'icon-good'})  else 0
                type_flag =  top_num + good_num
            except Exception ,e:
                with open("log.txt",'a+') as f:
                    f.writelines(str(id))



            page_list.append((id,name,tie_url,author,type_flag))

        insert_list = checks_tieba_todb(page_list)
        page_list = []


        if insert_list!=[]:
            insert_baidu_tieba_todb(insert_list)






