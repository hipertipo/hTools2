# test cap & join options

from hTools2.modules.nodebox import capstyle, joinstyle, draw_cross

def cap_join_options((x, y), (cap, join)):

    push()
    scale(540 * .001 )
    translate(x, y)
    nofill()
    autoclosepath(False)
    strokewidth(90)
    beginpath(58, 100)
    lineto(251, 100)
    lineto(64, 300)
    lineto(300, 300)
    p = endpath()
    p = capstyle(p, cap) 
    p = joinstyle(p, join)
    drawpath(p)
    pop()

x = -16
y = -123
c = 1.0 / 3

R = 0
G = 1
B = 1

for cap in range(3):
    _x = x
    for join in range(3):
        _color = color(c * cap, c * join, .5, .5) 
        stroke(_color)
        cap_join_options((_x, y), (cap, join))
        _x += 376
    y += 352
