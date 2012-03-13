colors = ximport('colors')

from hTools2.modules.color import *

x = 22
y = x
w = 80
h = w
s = 4 + w

_x = x
for _color in solarized('dark'):
    fill(RGB_to_nodebox_color(_color, _ctx))
    rect(x, y, w, h)
    x += s

x = _x
y += s
for _color in solarized('bright'):
    fill(RGB_to_nodebox_color(_color, _ctx))
    rect(x, y, w, h)
    x += s
    
x = _x
y += s
for _color in solarized('colors'):
    fill(RGB_to_nodebox_color(_color, _ctx))
    rect(x, y, w, h)
    x += s    

x = _x
y += s
for _color in solarized('content'):
    fill(RGB_to_nodebox_color(_color, _ctx))
    rect(x, y, w, h)
    x += s    
