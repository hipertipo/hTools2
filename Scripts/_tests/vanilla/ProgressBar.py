# [h] progress bar demo

from vanilla import *

class ProgressBarDemo(object):

    def __init__(self):
        self.w = Window((200, 65))
        self.w.bar = ProgressBar((10, 10, -10, 16))
        self.w.button = Button((10, 35, -10, 20), "Go!", callback=self.showProgress)
        self.w.open()

    def showProgress(self, sender):
        #import time
        self.w.bar.set(0)
        for i in range(10):
            self.w.bar.increment(10)
            #time.sleep(.2)

ProgressBarDemo()