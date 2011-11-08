from mojo.drawingTools import *
from mojo.events import addObserver

class DrawTest:

    def __init__(self):
        ## add an observer for the draw event
        addObserver(self, "drawSomething", "draw")

    def drawSomething(self, glyph, info):
        ## draw something the glyph view
        oval(100, 100, 100, 100)

DrawTest()