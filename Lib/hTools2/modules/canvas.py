# objects to draw a DrawBot-like canvas in RoboFont
# temporary, these will be added to mojo.drawingTools
# code by Frederik Berlaen, 26/11/2010

from AppKit import *
from vanilla import Group, ScrollView
from mojo.drawingTools import *

class CanvasNSView(NSView):
    
    def __new__(cls, *arg, **kwargs):
        self = cls.alloc().init()
        return self

    def __init__(self, (w, h), drawCallback):
        self.setFrame_(NSMakeRect(0, 0, w, h))
        self._drawCallback = drawCallback
        
    def drawRect_(self, rect):
        NSColor.whiteColor().set()
        NSRectFill(rect)
        save()
        self._drawCallback()
        restore()

    def update(self):
        self.setNeedsDisplay_(True)

class Canvas(Group):
    
    def __init__(self, posSize, canvasSize, drawCallback):
        super(Canvas, self).__init__(posSize)
        self._view = CanvasNSView(canvasSize, drawCallback)
        self.scrollView = ScrollView((0, 0, 0, 0), self._view, backgroundColor=NSColor.grayColor(), hasHorizontalScroller=False, hasVerticalScroller=False)

    def update(self):
        self._view.update()
