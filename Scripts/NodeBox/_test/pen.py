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
strokewidth(524 * .01)
beginpath()
g.draw(pen)
p = endpath(draw=False)
drawpath(p)

'''
# http://nodebox.net/code/index.php/Manipulating_Paths

nostroke()
oval_size = 19
for point in p:
    # print point
    if point.cmd == 0:
        fill(1, 0, 0)
    elif point.cmd == 1:
        fill(0, 1, 0)
    else:
        fill(0, 0, 1)
    oval(point.x - (oval_size/2), point.y - (oval_size/2), oval_size, oval_size)

stroke(1, 0, 0)
strokewidth(2)
nofill()

'''
