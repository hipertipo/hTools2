# [h] simple RoboFont canvas test

from vanilla import *
from mojo.drawingTools import *
from mojo.canvas import Canvas

# from hTools2.modules.canvas import *

class CanvasTest:

    _width = 300
    _height = 300
    _top = 75
    _padding = 0
    _grid = 7
        
    def __init__(self):
        self.w = Window((self._width, self._height))
        self.w.c = Canvas((self._padding, self._top, -self._padding, -self._padding*2), (self._width, self._height), self.draw)
        self.w.slider_x = Slider((10, 10, -10, 20), callback=self.slider_x_callback)
        self.w.slider_y = Slider((10, 40, -10, 20), callback=self.slider_y_callback)
        self.w.open()
                
    def draw(self):
        fill(.9)
        x = 0
        while x < self._width:
            rect(0, x, self._height, 1)
            x += self._grid
        y = 0
        while y < self._height:
            rect(y, 0, 1, self._width)
            y += self._grid

    def slider_x_callback(self, sender):
        x = sender.get()
        print x
        # fill(0, 1, 0)
        # self.w.c.rect(x, x, 20, 20)
        
    def slider_y_callback(self, sender):
        y = sender.get()
        print y


CanvasTest()

