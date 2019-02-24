#coding=utf-8
import requests
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
url = "http://www.biquge.lu/book/1082/"

res_session = requests.session()

respons = res_session.get(url)
respons.encoding = 'gbk'


soup = BeautifulSoup(respons.text,"html.parser")
print soup.find('div',{'class':"info"})