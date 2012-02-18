hTools = ximport("hTools")

'''draw EGlyph array'''

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.tools.ETools_NodeBoxTools import EString, drawGrid
from hTools.tools.ETools import ESpace

# context
C = _ctx
C.size(2000, 800)
C.background(0)

# ESpace
s = ESpace()
s.styles =  [ 'B' ]
s.heights = [ '17','16','15','14','13','12','11','10','09' ] # '08','07','06','05','04','03','02','01'
s.weights = [ '11','21','31','41' ]
s.widths =  [ '1','2','3','4' ]

# EString
S = EString(s)
S._labels_Weights = 4
S._labels_Widths = 8
S._labels_Heights = 3
S._drawVMetrics = False
S._drawHMetrics = False

# draw!
S.draw(C, (10,32), ('/n/zero/three/p/space', 'gString'), _anchors=False)

# drawGrid(C)