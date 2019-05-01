#coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

import glob
from os import path
import os
from aip import AipOcr
from PIL import Image

dict_show = {u'log_id': 116329545525502076L, u'words_result_num': 24, u'words_result': [{u'words': u'4|55'}, {u'words': u'554|5'}, {u'words': u'\u76f4154|5'}, {u'words': u'1645'}, {u'words': u'43'}, {u'words': u'l3'}, {u'words': u'24|5554'}, {u'words': u'56545'}, {u'words': u'2t|2665'}, {u'words': u'4'}, {u'words': u'4|5'}, {u'words': u'24321|2'}, {u'words': u'000'}, {u'words': u'0'}, {u'words': u'0'}, {u'words': u'0000|42525125151212525555'}, {u'words': u'6-sis4|5'}, {u'words': u'1245124512000000000|\u3002\u3002\u30020'}, {u'words': u'24|555'}, {u'words': u'554|5\xb1'}, {u'words': u'4|55144|?512'}, {u'words': u'\u70b9'}, {u'words': u'5.4'}, {u'words': u'k\u4ee5k'}]}

for strs in dict_show['words_result']:
    print strs['words']