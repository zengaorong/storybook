from datetime import datetime

with open("time.txt",'a+') as f:
    f.writelines(str(datetime.now())+'\n')