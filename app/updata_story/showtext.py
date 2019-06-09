#coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import time
from bs4 import BeautifulSoup
from data.operatedb import check_chapter_todb
from storys import story_spider_for_biequge
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

data_text = u"\\xE6\\x95\\x9E\\xE5\\xA4\\xA7".decode('gbk')
print data_text