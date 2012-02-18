#--- imports

hTools = ximport("hTools")
colors = ximport("colors")

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import ELine

# script

C = _ctx
C.size(1200, 800)
C.background(0)

# ESpace

heights = ['09','13','17']
style = 'B'
weight = '11'
width = '3'

# groups

iGroup = 1

p = hProject('Elementar')
_groups = p.groupsFromEncoding
_groupName = p.groupsOrder[iGroup]
#_glyphName = _groups[_groupName][iGlyph]
#print "%s, %s" % ( _groupName, _glyphName )

# glyph groups 

x, y = 20, 30

# draw group name
C.fill(.7)
font('EMono13', 13)
text(_groupName, x, y)

# draw glyphs
for height in heights:
    EName = 'E' + style + height + weight + width + 'A'
    e = ELine(EName, C)
    e.gNames = _groups[_groupName]
    e.draw((x+220,y), parse=False)
    y += int(e.height)+5
