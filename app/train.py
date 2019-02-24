import threading
import random
import time

def __print_num(count_num):
    print count_num
    time.sleep(random.randint(3,6))


if __name__ == "__main__":
    threading_downs = []
    for num in range(0,20):
        threading_down = threading.Thread(target=__print_num,args=(num,))
        threading_downs.append(threading_down)
        threading_down.start()

    [t.join() for t in threading_downs]



# # coding:utf-8
# import threading
# import time
#
# def action(arg):
#     time.sleep(1)
#     print  'sub thread start!the thread name is:%s\r' % threading.currentThread().getName()
#     print 'the arg is:%s\r' %arg
#     time.sleep(1)
#
# for i in xrange(4):
#     t =threading.Thread(target=action(i))
#     t.start()
#
# print 'main_thread end!'