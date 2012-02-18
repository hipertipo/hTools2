# Elementar iPad sample generator

hTools = ximport("hTools")
colors = ximport("colors")

#reload(hTools.tools.ETools)
#reload(hTools.tools.ETools_NodeBoxTools)

from hTools.tools.ETools import EName, ESpace
from hTools.tools.ETools_NodeBoxTools import EParagraph, ESample, drawHorzLine

def makeSample(_EName, C):
    x1 = 1
    p = EParagraph(_EName, C) 
    p.pWidth = 450
    p.leading = 5
    p.c = C.color(1)
    p.txt = txt
    p.zoom = 1
    shift = {
        '01' : 7,
        '02' : 6,
        '03' : 5,
        '04' : 4,
        '05' : 3,
        '06' : 2,
        '07' : 1,
        '08' : 0,
        '09' : -1,
        '10' : -2,
        '11' : -3,
        '12' : -4,
        '13' : -5,
        '14' : -6,
        '15' : -7,
        '16' : -8,
        '17' : -9,
        }
    y1 = shift[p.height]
    p.draw((x1,y1), frame=0, bound=0, box=0, baseline=0, glyphs=1, breakLines=0)

def generateSamples(space):
    space.compile()
    space.buildNames()
    print 'generating samples...'
    for E in space.ENames:
        fileName = '/Users/gferreira0/Dropbox/Elementar/iPad app/samples/text/%s_text.png' % E
        # print '\tsaving %s...' % fileName
        makeSample(E, C)
        C.canvas.save(fileName)
        C.canvas.clear()
    print '...done.\n'

# canvas setup

size(568, 352)
background(0)
C = _ctx
txt = open('text.txt', 'r').read()

# single sample settings

eName = 'EB13113A'
E = EName(eName)

# batch generation settings

S = ESpace()
S.styles = [ 'B', 'H', 'S' ]
S.weights = [ '11', '21', '31', '41' ]
S.widths = [ '1', '2', '3', '4' ]
S.types = [ 'A' ]
S.propWidths = True

makeSample(eName, C)
#generateSamples(S)
#drawHorzLine(13, C, s=.5, c=color(0,1,0))
