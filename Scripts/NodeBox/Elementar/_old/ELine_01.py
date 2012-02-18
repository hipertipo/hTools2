# import

hTools = ximport("hTools")

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.objects import hProject
from hTools.tools.ETools_NodeBoxTools import ELine
from hTools.tools.ETools import EWorld

# initialize canvas

C = _ctx
C.size(640, 480)
C.background(0)

# draw a cloud of ELines

w = EWorld()

for i in range(200):
    randomEFont = w.ufoNames[random(0, len(w.ufoNames)-1)] 
    L = ELine(randomEFont, C)
    L.gColor = color(1,random(),random(0,.5),random(0,.7))
    _x = random(-20, WIDTH)
    _y = random(-20, HEIGHT+20)
    L.draw((_x,_y))

