# import

hTools = ximport("hTools")
colors = ximport("colors")

# Elementar iPad sample generator

from hTools.tools.ETools import EName, ESpace
from hTools.tools.ETools_NodeBoxTools import EPrism, ESample, drawGrid

def makeSample(_EName, clrs=False):
    x, y = 127, 115
    xShift = 200
    if clrs == False:
        m = 0
    else:
        m = 2
    styles = [ 'B', 'H', 'S' ]
    for st in range(len(styles)):
        p = EPrism(_EName, C)
        p.buildColors()
        p.zoom = 1
        p.xGrid = 40
        p.yGrid = 10
        p.yStep = 10
        p.currentFont.style = styles[st]
        p.widths = ['1', '2', '3', '4']
        p.weights = ['11', '21', '31', '41']
        p.colorMode = 'RGB'
        p.draw((x + (xShift*st), y), pos=0, mode=1, ufo=True)

# canvas setup

C = _ctx
C.size(800, 600) # (160, 433)
C.background(0)
c = True # color switch includes destination folder
# drawGrid(C)

# define current font

eName = 'EB17411A'
E = EName(eName)
makeSample(E, clrs=c)
