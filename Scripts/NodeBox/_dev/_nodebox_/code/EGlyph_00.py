colors = ximport("colors")

'''batch save pdf EGlyph samples'''

import time
from hTools.objects.hProject import hProject
from hTools.tools.ETools_NodeBoxTools import EString, drawGrid
from hTools.tools.ETools import ESpace

def drawString(eString, gName, ctx):
    # drawGrid(ctx)
    _string = "/%s/space" % gName
    eString.draw(C, (20,25), (_string, 'gString'), _anchors=0)

def batchGenerateSamples(space, groupNumbers):
    print "batch generating samples..."
    for I in groupNumbers:
        _groupName = p.groupsOrder[I]
        for i in range(len(_groups[_groupName][:])): 
            # set EString
            S = EString(space)
            S._labels_Weights = 5
            S._labels_Widths = 10
            S._labels_Heights = 7
            # draw EString
            _glyphName = _groups[_groupName][i]
            _fileName = '%s/%s_%s_%s_%s.png' % ( destFolder, space.styles[0], I, i, _glyphName)
            drawString(S, _glyphName, C)
            # save & clear
            canvas.save(_fileName)
            canvas.clear()
    print "...done."

# set context
C = _ctx
C.size(360, 180)
C.background(0)

# set ESpace
s = ESpace()
s.styles =  ['B']
s.heights = ['09','10','11','12','13','14','15','16','17']  
s.weights = ['11','21','31','41']
s.widths =  ['1','2','3','4']

# set groups
p = hProject('Elementar')
_groups = p.groupsFromEncoding
allGroups = []
for i in range(28):
    allGroups.append(i+1)

destFolder = u"/Users/gferreira0/Dropbox/Elementar/nodebox/imgs"

# batch draw & save EStrings
_start = time.clock()
batchGenerateSamples( s, [1] )
_end = time.clock()
_time = _end - _start 
print "total generation time: %s seconds" % _time