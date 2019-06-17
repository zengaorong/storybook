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

data_text =u'\u5251\u6765'
print data_text