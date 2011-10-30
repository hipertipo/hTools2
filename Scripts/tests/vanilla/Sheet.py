from vanilla import *

class WindowDemo(object):

    def __init__(self):
        self.w = Window((200, 70), "Window Demo")
        self.w.myButton = Button((10, 10, -10, 20), "My Button")
        self.w.myTextBox = TextBox((10, 40, -10, 17), "My Text Box")
        #self.w.myList = List((0, 0, 100, 100), ["A", "B", "C"])
        self.w.open()

w = WindowDemo()
