hTools = ximport("hTools")
colors = ximport("colors")

'''batch save samples for EGlyph styles'''

import time

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import EString, drawGrid
from hTools.tools.ETools import ESpace

# set context
C = _ctx
C.size(320, 600)
C.background(0)

# set ESpace
_styles = [ 'B', 'H', 'S' ]

# set group
p = hProject('Elementar')
_groups = p.groupsFromEncoding
allGroups = []
for i in range(28):
    allGroups.append(i+1)

# batch draw & save EStrings
groupNumbers = [ 1 ]
print "batch generating samples..."
_start = time.clock()
for I in groupNumbers:
    _groupName = p.groupsOrder[I]
    for i in range(len(_groups[_groupName][:1])): 
        drawGrid(C)
        # draw EGlyph
        _gName = _groups[_groupName][i]
        _fileName = '/Users/gferreira0/Dropbox/Elementar/proofs/%s_%s_%s.png' % ( I, i, _gName)
        _string = "/%s/space" % _gName
        x, y = 50, 50
        for _style in _styles:
            # define space
            s = ESpace()
            s.styles =  [ _style ]
            s.heights = [ '09','10','11','12','13','14','15','16','17' ]  
            s.weights = [ '11','21','31','41' ]
            s.widths =  [ '1','2','3','4' ]
            # define string
            S = EString(s)
            S._labels_Weights = 5
            S._labels_Widths = 10
            S._labels_Heights = 7
            S._drawHMetrics = False
            S._drawVMetrics = False
            S.draw(C, (x,y), (_string, 'gString'), _anchors=0)
            y += 166
        # save & clear
        #canvas.save(_fileName)
        #canvas.clear()
_end = time.clock()
print "...done."
print "total generation time: %s seconds" % (_end - _start)
