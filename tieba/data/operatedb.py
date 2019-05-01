#coding=utf-8
import sys
import MySQLdb
import os
import re
import uuid
import platform
from copy import deepcopy

reload(sys)
sys.setdefaultencoding('utf-8')
dataname = "spider"
host='120.79.217.238'

def insert_baidu_tieba_todb(list):
    conn= MySQLdb.connect(
        host= '120.79.217.238',
        port = 3306,
        user='root',
        passwd='7monthdleo',
        db = dataname,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "insert into baidu_tieba(id,name,tie_url,author,type_flag)value(%s,%s,%s,%s,%s)"

    cur.executemany(sqli,list)
    # for data in list:
    #     cur.execute(sqli,[data[0],data[1],data[2],data[3],data[4]])
    conn.commit()
    conn.close()

def checks_tieba_todb(page_list):
    conn= MySQLdb.connect(
            host= '120.79.217.238',
            port = 3306,
            user='root',
            passwd='7monthdleo',
            db = dataname,
            charset='utf8'
        )
    cur = conn.cursor()
    sqli =  "SELECT * from baidu_tieba WHERE id = %s"
    # tuple_id = tuple(id_list)
    # print tuple_id
    tuple_id_str = ""
    out_list = deepcopy(page_list)
    for page in page_list:
        result = cur.execute(sqli,[str(page[0])])
        if result:
            out_list.remove(page)
        else:
            pass

    conn.commit()
    conn.close()
    return out_list

def get_qupu_from_id_todb(id):
    conn= MySQLdb.connect(
        host= '120.79.217.238',
        port = 3306,
        user='root',
        passwd='7monthdleo',
        db = dataname,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "SELECT * from baidu_tieba WHERE id =%s"
    resut = cur.execute(sqli,[id])
    sellect_list = cur.fetchmany(resut)

    conn.commit()
    conn.close()
    return sellect_list

def get_qupu_url_bynum_todb(nums):
    conn= MySQLdb.connect(
        host= '120.79.217.238',
        port = 3306,
        user='root',
        passwd='7monthdleo',
        db = dataname,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "SELECT id,tie_url from baidu_tieba where type_spider<>3 LIMIT %s"
    resut = cur.execute(sqli,[nums])
    sellect_list = cur.fetchmany(resut)

    conn.commit()
    conn.close()
    return sellect_list

def set_qupu_type_spider_todb(id_list):
    conn= MySQLdb.connect(
        host= '120.79.217.238',
        port = 3306,
        user='root',
        passwd='7monthdleo',
        db = dataname,
        charset='utf8'
    )
    cur = conn.cursor()
    sqli =  "UPDATE  baidu_tieba  set type_spider = 3 WHERE id = %s"
    cur.execute(sqli,[id_list])

    conn.commit()
    conn.close()