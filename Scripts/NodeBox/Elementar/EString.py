# [e] draw EString

from hTools.objects.hProject import hProject
from hTools.tools.ETools import ESpace
from hTools.tools.ETools_NodeBoxTools import EString, drawGrid

C = _ctx
C.size(1800, 800)
C.background(0)

s = ESpace()
s.styles = [ 'B' ]
s.heights = s.heights[8:]
s.weights = s.weights[:1]
s.widths = s.widths[:]
s.update()
s.propWidths = True

glyphs = '/a/space'

S = EString(s)
S.draw(C, (20,20), (glyphs, 'gString'))

# drawGrid(C)
