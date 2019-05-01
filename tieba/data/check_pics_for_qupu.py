import pytesseract
import glob
from PIL import Image
from str_check_qupu import pic_str_check_qupu
import sys
import os
import shutil


def check_pics_for_qupu(pic_file,url):
    has_pic_qupu = False
    for picfile in glob.glob("%s/*"%pic_file):
            if os.path.getsize(picfile) < 1024*10*3:
                continue
            try:
                strs = pytesseract.image_to_string(Image.open(picfile).convert('RGB'))
                if pic_str_check_qupu(strs):
                    shutil.move(picfile,pic_file.split('/')[0])
                    has_pic_qupu = True
            except Exception ,e:
                with open("log/errorlog",'a+') as f:
                    f.writelines(url + '\t' + str(e) + '\n')

    return has_pic_qupu