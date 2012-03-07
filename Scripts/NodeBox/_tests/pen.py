# simple pen example

from robofab.world import RFont
from hTools2.modules.pens import NodeBoxPen

ufo_path = u"/fonts/_Publica/_ufos/Publica_55.ufo"
ufo = RFont(ufo_path)
pen = NodeBoxPen(ufo, _ctx)
g = ufo['a']
translate(11, 540)
transform('CORNER')
scale(97 * .01)
fill(.9)
stroke(.5)
strokewidth(226 * .01)
beginpath()
g.draw(pen)
p = endpath(draw=False)
drawpath(p)

# http://nodebox.net/code/index.php/Manipulating_Paths

nostroke()
oval_size = 10
for point in p:
    x = point.x - (oval_size/2)
    y = point.y - (oval_size/2)
    if point.cmd == 0:
        fill(1, 0, 0)
        oval(x, y, oval_size, oval_size)
    elif point.cmd == 1:
        fill(0, 1, 0)
        oval(x, y, oval_size, oval_size)
    elif point.cmd == 2:
        fill(0, 0, 1)
        oval(x, y, oval_size, oval_size)
