#coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
import os
from os import path
from ..data.str_check_qupu import str_check_qupu
from collections import OrderedDict
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def down_tizhi_forqupu(down_url,file_name,session_tieba):
    url_page = down_url
    respons = session_tieba.get(url_page)
    soup = BeautifulSoup(respons.text,'html.parser')

    #生成楼层的json数据列表
    lou_ceng_post_list = []
    # 帖子是否存在下一页
    has_next = True
    # 对于包含多个曲谱的帖子 进行计数
    down_qupu_str_nums = 1

    if soup.find('div',{"class":'louzhubiaoshi j_louzhubiaoshi'}):
        str_tiezi_author = soup.find('div',{"class":'louzhubiaoshi j_louzhubiaoshi'})['author']
    if soup.find('div',{"class":'p_author_name j_user_card vip_red '}):
        str_tiezi_author = soup.find('div',{"class":'p_author_name j_user_card vip_red '})['author']
    else:
        str_tiezi_author = ""
    str_tiezi_url = url_page

    if soup.find('h3',{'class':'core_title_txt pull-left text-overflow '}):
        str_tiezi_title = soup.find('h3',{'class':'core_title_txt pull-left text-overflow '}).string
    if soup.find('h3',{'class':'core_title_txt pull-left text-overflow   vip_red '}):
        str_tiezi_title = soup.find('h3',{'class':'core_title_txt pull-left text-overflow   vip_red '}).string
    else:
        str_tiezi_title = ""

    # 曲谱是否包含图片
    has_str_qupu = False
    image_url_list = []

    while has_next:
        respons = session_tieba.get(url_page)
        soup = BeautifulSoup(respons.text,'html.parser')
        tieba_lou_list = soup.find_all('div',class_= ["l_post l_post_bright j_l_post clearfix "])

        #获取楼层的信息
        for tie_lou in tieba_lou_list:
            str_lou_ceng_num = ""
            str_text = ""
            img_url_list = []
            str_author = ""
            str_datetime = ""

            content = tie_lou.find('div',{'class','d_post_content j_d_post_content '})
            if content==None:
                continue
            # print content
            str_text = content.get_text()
            if str_check_qupu(str_text):
                with open('%s/%s_%s.txt'%(file_name,file_name,down_qupu_str_nums),'w') as f:
                    temp_str = ""
                    for key in content:
                        if type(key).__name__ == "Tag":
                            if key.name == "br":
                                temp_str = temp_str + '\n'
                            if key.name == "a":
                                if key.string!=None:
                                    temp_str = temp_str + key.string
                        if type(key).__name__ == "NavigableString":
                            if key.string!=None:
                                temp_str = temp_str + key.string.replace('            ',"")

                    f.writelines(temp_str)
                    down_qupu_str_nums = down_qupu_str_nums + 1
                    has_str_qupu = True

            if tie_lou.find('a',{'class':'p_author_name j_user_card'})!=None:
                str_author = tie_lou.find('a',{'class':'p_author_name j_user_card'}).string
            elif tie_lou.find('a',{'class':'p_author_name sign_highlight j_user_card'})!=None:
                str_author = tie_lou.find('a',{'class':'p_author_name sign_highlight j_user_card'}).get_text()

            # 获取楼层 时间 数据 （该处要分两种情况）
            # 存在删楼情况 需要判断 同时直接跳过
            if tie_lou.find('div',{'class':'post-tail-wrap'}):
                tips_list = tie_lou.find('div',{'class':'post-tail-wrap'}).find_all('span',{'class':'tail-info'})
            else:
                continue

            if len(tips_list)==3:
                str_lou_ceng_num = tips_list[1].string
                str_datetime = tips_list[2].string
            if len(tips_list)==2:
                str_lou_ceng_num = tips_list[0].string
                str_datetime = tips_list[1].string

            pics_list = content.find_all('img',{'class':'BDE_Image'})
            temp_num = 0
            for pics in pics_list:
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


        limit_page = soup.find('li',{'class':'l_pager pager_theme_5 pb_list_pager'})
        if limit_page==None:
            has_next = False
            continue
        len(limit_page.find_all('a'))
        if len(limit_page.find_all('a'))>0 and limit_page.find_all('a')[-2].string == '下一页':

            next_url = limit_page.find_all('a')[-2]['href']
            print next_url
            url_page = "https://tieba.baidu.com" + next_url
        else:
            has_next = False




    json_out = OrderedDict()
    json_out["author"] = str_tiezi_author
    json_out["title"] = str_tiezi_title
    json_out["url"] = str_tiezi_url
    json_out["posts"] = lou_ceng_post_list



    with open("%s/%s.json"%(file_name,file_name),"w" ) as f:
        json.dump(json_out,f,indent=4,ensure_ascii=False)
        print("加载入文件完成...")


    if image_url_list:
        outdir = '%s/tmp_%s'%(file_name,str(10001))
        if not path.exists(outdir):
            os.mkdir(outdir)
        temp_num = 0

        for pics in image_url_list:
            try:
                ir = session_tieba.get(pics)
                open(r'%s/%s.jpg'%(outdir,temp_num) , 'wb').write(ir.content)
                temp_num = temp_num + 1
            except Exception,e:
                with open("log/urlerrolog.txt",'a+') as f:
                    f.writelines(pics + '\t' + str(e) + '\n')

    return has_str_qupu