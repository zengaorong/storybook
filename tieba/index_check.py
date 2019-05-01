#coding=utf-8
import requests
import sys
from tieba.down_date.down_tizhi_forqupu import down_tizhi_forqupu
from tieba.data.check_pics_for_qupu import check_pics_for_qupu
from data.operate import mkdir
from data.operatedb import get_qupu_url_bynum_todb,set_qupu_type_spider_todb
import os
import shutil
reload(sys)
sys.setdefaultencoding('utf-8')



tiezi_data_list = get_qupu_url_bynum_todb(3600)
id_list = []
session_tieba = requests.session()
session_tieba.keep_alive = False
for tiezi_data in tiezi_data_list:
    print tiezi_data[1]
    url = tiezi_data[1]
    file_name = url.split('/')[-1]
    mkdir(file_name)
    has_str_qupu = down_tizhi_forqupu(url,file_name,session_tieba)
    has_pic_qupu = check_pics_for_qupu("%s/tmp_10001"%file_name,url)
    if os.path.exists("%s/tmp_10001"%file_name):
        shutil.rmtree("%s/tmp_10001"%file_name)

    try:

        if not has_str_qupu and  not has_pic_qupu:
            shutil.move(file_name,"qupu/has_not_qupu")
        if has_str_qupu and  not has_pic_qupu:
            shutil.move(file_name,"qupu/has_str_qupu")
        if not has_str_qupu and  has_pic_qupu:
            shutil.move(file_name,"qupu/has_pic_qupu")
        if has_str_qupu and  has_pic_qupu:
            shutil.move(file_name,"qupu/has_str_pic_qupu")
    except:
        pass

    try_time =  2
    while try_time >0:
        try:
            set_qupu_type_spider_todb(tiezi_data[0])
            try_time = 0
        except Exception ,e:
            try_time = try_time - 1

# print check_pics_for_qupu("3120453475/tmp_100001","as")
