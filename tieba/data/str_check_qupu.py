#coding=utf-8
import requests
import sys

qupu_list = ['1','2','3','4','5','6','7','#','(',')','[',']','|']

check_str_test = '''
1=C3235 12125 1222343
43466561 1431122
3235 12125 1222343
2#123434543231
555#24#24 4#622454#22#2
#21#21#245#2 #21#21#245#55
#6#6#6#6#6#6#55#5#6#6
114544566
5444#6656
234154#6#6#66455
114544566
5444#6(1)6545
234154 (1)#66454344
'''



def str_check_qupu(check_str):
    check_nums = 0
    for key in check_str:
        if key in qupu_list:
            check_nums =  check_nums + 1
            if check_nums > 50:
                print check_nums
                return True

    return False

def pic_str_check_qupu(check_pis_str):
    check_nums = 0
    for key in check_pis_str:
        if key in qupu_list:
            check_nums =  check_nums + 1
            if check_nums > 15:
                return True
    return False