hTools = ximport("hTools")

'''batch save pdf samples for EGlyph styles'''

import time

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import EString, drawGrid
from hTools.tools.ETools import ESpace

# set context
C = _ctx
C.size(720, 400)
C.background(0)

# set groups
p = hProject('Elementar')
_groups = p.groupsFromEncoding
allGroups = []
for i in range(len(_groups)):
    allGroups.append(i+1)

# set style
styles = [ 'B', 'H', 'S' ]
vMetrics = False
hMetrics = False

# batch draw & save EStrings
groupNumbers = [ 1 ]

# draw EGlyph
_start = time.clock()
print "batch generating samples..."

destFolder = u"/Users/gferreira0/Dropbox/Elementar/nodebox/imgs"

for I in groupNumbers:
    group = p.groupsOrder[I]
    if group not in [ 'bug', 'invisible', 'spaces' ]:
        print group
        for i in range(len(_groups[group])):
            gName = _groups[group][i]
            _string = "/%s/space" % gName
            _fileName = '%s/%s_%s_%s.png' % ( destFolder, I, i, gName)
            drawGrid(C)
            x, y = 40, 40
            count = 0
            for style in styles:
                # define space
                s = ESpace()
                s.styles =  [ style ]
                s.heights = [ '17','16','15','14','13','12','11','10','09' ]  
                s.weights = [ '11','21','31','41' ]
                s.widths =  [ '1','2','3','4' ]
                # define string
                S = EString(s)
                S._labels_Weights = 5
                S._labels_Widths = 10
                S._labels_Heights = 7
                S.gString = _string
                if count != 0:
                    S._drawVMetrics = vMetrics
                S._drawHMetrics = hMetrics
                # draw and update state
                S.draw(C, (x,y), (_string, 'gString'), _anchors=0)
                x += 200
                count += 1
            # save & clear
            canvas.save(_fileName)
            canvas.clear()
_end = time.clock()
print "...done."
print "total generation time: %s seconds" % (_end - _start)

