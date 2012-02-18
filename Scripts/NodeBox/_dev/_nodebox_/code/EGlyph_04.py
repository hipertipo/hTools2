hTools = ximport("hipertipo")
colors = ximport("colors")

'''batch save pdf EGlyph samples'''

import time

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import EString, drawGrid
from hTools.tools.ETools import ESpace

def drawString(eString, gName, ctx):
    drawGrid(ctx)
    eString.gString = "/%s/space" % gName
    eString.draw(C, (20,25), _anchors=0)

def lc2sc(gName):
    return '%s.sc' % gName

def lc2uc(gName):
    return gName.upper()

def batchGenerateSamples2(context, space, script, group):
    p = hProject('Elementar')
    _groups = p.groupsFromEncoding
    _group = '%s_lc_%s' % (script, group)
    print "batch generating glyph samples..."
    for gName in _groups[_group]:
        uc, lc, sc  = lc2uc(gName), gName, lc2sc(gName)
        # set EString
        S = EString(space)
        S.gString = "/%s/%s/%s/space" % (uc,sc,lc)
        S._labels_Weights = 4
        S._labels_Widths = 8
        S._labels_Heights = 3
        # draw EString
        drawGrid(context)
        S.draw(context, (10,20), _anchors=0)
        # save & clear
        _fileName = '_imgs/EGlyphs/_cases/%s.pdf' % gName
        canvas.save(_fileName)
        canvas.clear()
    print "...done."

# set context
C = _ctx
C.size(680, 170)
C.background(0)

# set ESpace & script
s = ESpace()
s.styles =  [ 'B' ]
s.heights = [ '09', '10', '11', '12', '13', '14', '15', '16', '17' ]
s.weights = [ '11', '21', '31', '41' ]
s.widths =  [ '1', '2', '3', '4' ]
script = 'latin'
group = 'basic'

# batch draw & save EStrings
_start = time.clock()
batchGenerateSamples2(C, s, script, group)
_end = time.clock()
_time = _end - _start 
print "total generation time: %s seconds" % _time
