#coding=utf-8
from datetime import datetime
import requests
import ssl
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

# with open("time.txt",'a+') as f:
#     f.writelines(str(datetime.now())+'\n')

head = {
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8"
}

url = "https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1"
# url = "https://www.biquge.lu/book/15676/"

# respons = requests.get(url,verify=False)
# with open("test.html",'w') as f:
#     f.writelines(respons.text)

# url = "http://www.biquge.lu/s.php?ie=gbk&s=15244670192641769733&q=1"
respons = requests.get(url,headers=head,timeout=30)
soup = BeautifulSoup(respons.text,"html.parser")
storys_page_list = soup.find_all("div",{"class":"book-mid-info"})
for key in storys_page_list:
    actor_name = key.find("a",{"class":"name"})
    story_name = key.find("a",{"target":"_blank"})
    print actor_name
    print story_name

# print respons.text
# with open("result.html","w") as f:
#     f.writelines(respons.text.replace('\r','\n'))

