#coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
import os
from os import path
from data.operatedb import get_qupu_from_id_todb
from data.str_check_qupu import str_check_qupu
from collections import OrderedDict
import json
reload(sys)
sys.setdefaultencoding('utf-8')

import pytesseract
import glob
from PIL import Image

# 爬虫情况代表帖子
# https://tieba.baidu.com/p/6111956958
session_tieba = requests.session()

# def read_pics_for_num(pic_file):
#     for picfile in glob.glob("%s/*"%pic_file):
#         try:
#             strs = pytesseract.image_to_string(Image.open(picfile))
#             print str_check_qupu(strs)
#             return strs

def get_lou_data(tieba_lou_list,session_tieba,qupu_is_pic,lou_ceng_post_list,image_url_list,down_qupu_str_nums):
    for tie_lou in tieba_lou_list:
        str_lou_ceng_num = ""
        str_text = ""
        img_url_list = []
        str_author = ""
        str_datetime = ""

        content = tie_lou.find('div',{'class','d_post_content j_d_post_content '})
        # print content
        str_text = content.get_text()
        if str_check_qupu(str_text):
            with open('6111956958_%s.txt'%down_qupu_str_nums,'w') as f:
                temp_str = ""

                for key in content:
                    if type(key).__name__ == "Tag":
                        if key.name == "br":
                            temp_str = temp_str + '\n'
                        if key.name == "a":
                            temp_str = temp_str + key.string
                    if type(key).__name__ == "NavigableString":
                        if key.string!=None:
                            temp_str = temp_str + key.string.replace('            ',"")

                f.writelines(temp_str)
                down_qupu_str_nums = down_qupu_str_nums + 1
                qupu_is_pic = False

        if tie_lou.find('a',{'class':'p_author_name j_user_card'})!=None:
            str_author = tie_lou.find('a',{'class':'p_author_name j_user_card'}).string
        elif tie_lou.find('a',{'class':'p_author_name sign_highlight j_user_card'})!=None:
            str_author = tie_lou.find('a',{'class':'p_author_name sign_highlight j_user_card'}).get_text()

        # 获取楼层 时间 数据 （该处要分两种情况）
        tips_list = tie_lou.find('div',{'class':'post-tail-wrap'}).find_all('span',{'class':'tail-info'})
        if len(tips_list)==3:
            str_lou_ceng_num = tips_list[1].string
            str_datetime = tips_list[2].string
        if len(tips_list)==2:
            str_lou_ceng_num = tips_list[0].string
            str_datetime = tips_list[1].string

        pics_list = content.find_all('img',{'class':'BDE_Image'})
        outdir = 'tmp'
        if not path.exists(outdir):
            os.mkdir(outdir)

        temp_num = 0
        for pics in pics_list:
            ir = session_tieba.get(pics['src'])
            open(r'%s/%s.jpg'%(outdir,temp_num) , 'wb').write(ir.content)
            temp_num = temp_num + 1
            img_url_list.append(pics['src'])
            image_url_list.append(pics['src'])
        # os.remove(outdir)
        lou_ceng = OrderedDict()
        lou_ceng["num"] = str_lou_ceng_num
        lou_ceng["author"] = str_author
        lou_ceng["datetime"] = str_datetime
        lou_ceng["text"] = str_text
        lou_ceng["image"] = img_url_list


        lou_ceng_post_list.append(lou_ceng)



if __name__ == "__main__":
    print get_qupu_from_id_todb(6111956958)

    url_page = "https://tieba.baidu.com/p/2680175091"
    respons = session_tieba.get(url_page)
    soup = BeautifulSoup(respons.text,'html.parser')

    lou_ceng_post_list = []
    # 帖子是否存在下一页
    has_next = True
    down_qupu_str_nums = 1

    str_tiezi_author = soup.find('div',{"class":'louzhubiaoshi j_louzhubiaoshi'})['author']
    str_tiezi_url = url_page
    str_tiezi_title = soup.find('h3',{'class':'core_title_txt pull-left text-overflow '}).string

    qupu_is_pic = True
    tieba_lou_list = soup.find_all('div',class_= ["l_post l_post_bright j_l_post clearfix "])

    image_url_list = []
    get_lou_data(tieba_lou_list,session_tieba,qupu_is_pic,lou_ceng_post_list,image_url_list,down_qupu_str_nums)

    while has_next:
        limit_page = soup.find('li',{'class':'l_pager pager_theme_5 pb_list_pager'})
        if limit_page.find_all('a')[-2].string == '下一页':

            next_url = limit_page.find_all('a')[-2]['href']
            print next_url
            url_page = "https://tieba.baidu.com" + next_url
            respons = session_tieba.get(url_page)
            soup = BeautifulSoup(respons.text,'html.parser')
            tieba_lou_list = soup.find_all('div',class_= ["l_post l_post_bright j_l_post clearfix "])
            get_lou_data(tieba_lou_list,session_tieba,qupu_is_pic,lou_ceng_post_list,image_url_list,down_qupu_str_nums)
        else:
            has_next = False


    json_out = OrderedDict()
    json_out["author"] = str_tiezi_author
    json_out["title"] = str_tiezi_title
    json_out["url"] = str_tiezi_url
    json_out["posts"] = lou_ceng_post_list



    with open("record.json","w" ) as f:
        json.dump(json_out,f,indent=4,ensure_ascii=False)
        print("加载入文件完成...")


    print qupu_is_pic
    if qupu_is_pic:
        outdir = 'tmp_%s'%(str(10001))
        if not path.exists(outdir):
            os.mkdir(outdir)
        temp_num = 0
        for pics in image_url_list:
            ir = session_tieba.get(pics)
            open(r'%s/%s.jpg'%(outdir,temp_num) , 'wb').write(ir.content)
            temp_num = temp_num + 1

    # read_pics_for_num("tmp_10001")