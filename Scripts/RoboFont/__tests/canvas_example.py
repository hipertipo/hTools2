from vanilla import *

from mojo.canvas import Canvas
from mojo.drawingTools import *

from robofab.world import RFont

import hTools2.modules.pens
reload(hTools2.modules.pens)

from hTools2.modules.pens import RoboFontPen

class WW:
    
    def __init__(self):
        self.size = 100
        self.font = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_Modular/_ufos/Modular_23-2-1.ufo"
        self.gName = "a"
        self.w = Window((400, 400), minSize=(200, 200))
        self.w.slider = Slider((10, 5, -10, 22), minValue=50, value=self.size, maxValue=200, callback=self.sliderCallback)
        self.w.canvas = Canvas((0, 30, -0, -0), canvasSize=(1000, 1000), delegate=self, acceptsMouseMoved=False)
        self.w.open()
    
    def sliderCallback(self, sender):
        self.size = sender.get()
        self.w.canvas.update()
        
    ## canvas delegate methods
    
    def draw(self):
        fill(0, 1, 0)
        rect(10, 10, self.size, self.size)
        fontSize(self.size/2.)
        text("size: %s" % self.size, self.size + 20, 10)
        #--------------------------------------
        # draw glyph
        save()
        fill(0, 0, 1)
        ufo = RFont(self.font, showUI=False)
        glyph = ufo[self.gName]
        pen = RoboFontPen(glyphSet=ufo)
        translate(100, 200)
        scale(10.0/64)
        newPath()
        glyph.draw(pen)
        drawPath()
        restore()
        #--------------------------------------
    
    def mouseDown(self, event):
        #print event
        print self.font
        print self.gName
        print

WW()    
        
