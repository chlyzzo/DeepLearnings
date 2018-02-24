#coding=utf-8

'''
Created on 2018年2月23日

@author: wenhaohu

线程学习
'''

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, 1, self.counter)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s:%d" % (threadName, time.ctime(time.time()),counter))
        counter -= 1
# 创建新线程
thread1 = myThread(1, "Thread-1", 10)
thread2 = myThread(2, "Thread-2", 2)

print(type(thread1))

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("退出主线程")
