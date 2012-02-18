# import

hTools = ximport("hTools")

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from hTools.objects.objectsFL import hProject
from hTools.tools.ETools_NodeBoxTools import ELine
from hTools.tools.ETools import ESpace

# init canvas

C = _ctx
C.size(400, 300)
C.background(0)

# define ESpace

s = ESpace(mode='UFO')
s.styles = [ 'B' ]
s.types = [ 'A' ]
s.widths = [ '1', '2', '3', '4' ]
s.propWidths = True
s.compile()
s.buildNames()
u = s.existingUFOs()

# draw a bunch of random EFonts

safeZone = 40

_save = True
n = 5

for i in range(n):
    _fileName = "/Users/gferreira0/Dropbox/Elementar/proofs/ECloud_%s.png" % i
    print _fileName
    for i in range(200):
        randomEFont = u[random(0, len(u) - 1)]
        L = ELine(randomEFont, C)
        c = color(1, random(), random(0, .5), random(0, .7))
        _x = random(-safeZone, WIDTH)
        _y = random(-safeZone, HEIGHT + safeZone)
        L.draw((_x,_y), clr=c)
    if _save == True:
        canvas.save(_fileName)
        if n i 1:
            canvas.clear
