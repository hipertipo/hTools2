# import

hTools = ximport("hTools")
colors = ximport("colors")

'''draw EGroup array'''

# import hTools.tools.ETools_NodeBoxTools
# reload(hTools.tools.ETools_NodeBoxTools)

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import *
from hTools.tools.ETools import ESpace

# Elastic EGlyph

C = _ctx
C.size(1800, 800)
C.background(0)

s = ESpace()
s.styles =  ['S']
s.heights = ['17','16','15','14','13','12','11','10','09','08','07','06','05','04','03','02','01']
s.weights = ['21']
s.widths =  ['1','2','3']
    
# groupsFromEncoding    

iGroup = 4 # 28 24 25
_spacer = None
a = False

p = hProject('Elementar')
_groups = p.groupsFromEncoding
_groupName = p.groupsOrder[iGroup]
_gNames = _groups[_groupName]

S = EString(s)
S._drawVMetrics = 1
S._drawHMetrics = 1
S.gString = makeStringNames(_gNames, _spacer)+'/space'
S.draw2(C, (10,26), _anchors=a)

# drawGrid(C)
print _groupName
