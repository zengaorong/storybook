#coding=utf-8
import base64

def get_picbase64(filename):
    with open(filename,'rb') as f:
        data_base64 = base64.b64encode(f.read())
        return data_base64


