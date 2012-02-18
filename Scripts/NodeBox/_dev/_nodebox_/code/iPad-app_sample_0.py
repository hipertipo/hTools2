# Elementar iPad sample generator

import hTools.tools.ETools
reload(hTools.tools.ETools)

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.tools.ETools import EName, ESpace
from hTools.tools.ETools_NodeBoxTools import EPrism, ESample


def makeSample(_EName):

    # font sample & font name
    x1, y1 = 50, 69
    S = ESample(_EName, C)
    S.sampleOffset = (24, 70)
    S.nameOffset = (23, -6)
    S.canvas = (440, 300)
    S.draw((x1, y1), pos=0)

    # prism
    x2, y2 = 798, 170
    p = EPrism(_EName, C)
    p.canvas = (190, 440)
    p.offset = (30, 61)
    p.zoom = 1
    p.xGrid = 40
    p.yGrid = 10
    p.yStep = 10
    p.widths = ['1', '2', '3', '4']
    p.weights = ['11', '21', '31', '41']
    p.heights = p.heights[0:int(_EName.height)]
    p.draw((x2, y2), pos=0)

    # zoom menu
    x3, y3 = 438, 62
    xStep = 36
    _zoomLevels = 3
    for z in range(_zoomLevels):
        if z != 0:
            C.fill(.3)
        else:
            C.fill(1, 0, 0)       
        t = u'%s×' % str(z+1)
        C.font('EMono13', 13)
        C.text(t, x3+(xStep*z), y3)        
    
    # styles menu
    x4, y4 = 830, 78
    xStep = 51
    _styles = [ 'B', 'H', 'S' ]
    C.font('EStyles', 52)
    count = 0
    for st in _styles:
        if st == _EName.style:    
            C.fill(1, 0, 0)
        else:
            C.fill(.4)
        C.text(st, x4 + (xStep*count), y4)
        count += 1

    # main menu
    x5, y5 = 70, 729
    C.font('EMenu', 18)    
    C.fill(1, 0, 0)
    C.text('demo', x5, y5)    
    C.fill(.3)
    C.text('about', x5+109, y5)


def generateSamples(space):
    space.compile()
    space.buildNames()
    print 'generating samples...'
    for f in space.ENames:
        fileName = 'imgs/%s.png' % f
        print '\tsaving %s...' % fileName
        makeSample(EName(f))
        C.canvas.save(fileName)
        C.canvas.clear()
    print '...done.\n'


# --------------------------------------------------
# canvas setup

size(1024, 680)
background(0)
C = _ctx

#image("app_demo.png", 0, 0, alpha=.5)

# --------------------------------------------------
# define current font

st = 'B'
ht = '15'
wt = '31'
wd = '1'

eName = 'E%s%s%s%sA' % ( st, ht, wt, wd ) 
E = EName(eName)

makeSample(E)

# --------------------------------------------------
# export & save pngs

sp = ESpace()
sp.styles = [ 'B', 'H', 'S' ]
sp.weights = [ '11', '21', '31', '41' ]
sp.widths = [ '1', '2', '3', '4' ]
sp.types = [ 'A' ]
sp.propWidths = True

# generateSamples(sp)

