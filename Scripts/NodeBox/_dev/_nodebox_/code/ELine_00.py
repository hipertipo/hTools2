# import

hTools = ximport("hTools")

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.tools.ETools_NodeBoxTools import ELine, allEGlyphs
from hTools.tools.ETools import EWorld

# initialize canvas

C = _ctx
C.size(400, 300)
C.background(0)

# draw ELine

L = ELine('EB13113A', C)

L.txt("Hello Default World!", mode="text")
L.draw((88, 62))

L.txt("Hello Green World!", mode="text")
L.draw((100, 168), color(0, 1, 0))

L.txt("/H/e.sc/l.sc/l.sc/o.sc/space/B/l/u/e/space/W/o/r/l/d/exclam")
L.draw((173, 117), color(0, 0, 1))
