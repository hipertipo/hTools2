hTools = ximport("hTools")
colors = ximport("colors")

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import ELine, allEGlyphs

# script

C = _ctx
C.size(1200, 1200)
C.background(0)

EName = 'EB17213A'

# glyph groups

x, y = 20, 30

print "total glyphs: %s" % len(allEGlyphs())

p = hProject('Elementar')
groups = p.groupsFromEncoding

counter = -1
for groupName in p.groupsOrder:
    counter += 1
    if groupName not in ['invisible','bug','spaces']:
        #print groupName
        e = ELine(EName, C)
        e.gNames = groups[groupName]
        # draw group name
        C.fill(.7)
        font('EMono13', 13)
        label = '%s %s' % (counter, groupName) 
        text(label, x, y)
        # draw group sample
        C.fill(1)
        e.draw((x+220,y))
        y += int(e.height)+7
