# Elementar iPad sample generator

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.tools.ETools import EName, ESpace
from hTools.tools.ETools_NodeBoxTools import EParagraph, ESample

def makeSample(_EName):
    '''generate sample using font API'''    
    x1, y1 = 20, 30
    S = ESample(_EName, C)
    S.sampleOffset = (0, 0)
    S.draw((x1, y1), pos=0)

def generateSamples(space):
    space.compile()
    space.buildNames()
    print 'generating samples...'
    for f in space.ENames:
        fileName = 'imgs/text/%s_text.png' % f
        print '\tsaving %s...' % fileName
        makeSample(EName(f))
        C.canvas.save(fileName)
        C.canvas.clear()
    print '...done.\n'

# --------------------------------------------------
# canvas setup

size(568, 352)
background(0)
C = _ctx
txt = open('text.txt', 'r').read()

# --------------------------------------------------
# define current font

eName = 'EB17421A'
E = EName(eName)
makeSample(E)

# --------------------------------------------------
# export & save pngs

sp = ESpace()
sp.styles = [ 'H', 'S' ]
sp.weights = [ '11', '21', '31', '41' ]
sp.widths = [ '1', '2', '3', '4' ]
sp.types = [ 'A' ]
sp.propWidths = True
#generateSamples(sp)

