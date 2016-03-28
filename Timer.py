# -*- coding: utf-8 -*-
__author__ = 'Ryan'

import threading
import time


class timer(threading.Thread):  # The timer class is derived from the class threading.Thread
    def __init__(self, func, args=(), num=1, interval=1):
        threading.Thread.__init__(self)
        self.thread_num = num
        self.interval = interval
        self.thread_stop = False
        self.func = func
        self.args = args

    def run(self):  # Overwrite run() method, put what you want the thread do here
        while not self.thread_stop:
            # print 'Thread Object(%d), Time:%s/n' % (self.thread_num, time.ctime())
            if self.args == 0:
                self.func()
            else:
                self.func(self.args)
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True