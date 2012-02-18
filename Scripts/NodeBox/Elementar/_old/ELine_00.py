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

L.gColor = color(1, 0, 0)
L.txt = "Hello Red World!"
L.draw((39,64))

L.gColor = color(0, 1, 0)
L.txt = "Hello Green World!"
L.draw((74,163))

