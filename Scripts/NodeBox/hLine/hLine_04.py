# [h] draw a line of glyphs from ufos

from robofab.objects.objectsRF import RFont

from hTools2.objects import hProject, hGlyph, hLine
from hTools2.modules.color import RGB_to_nodebox_color, solarized
from hTools2.modules.nodebox import make_alpha

bg_color = color(0) # RGB_to_nodebox_color(solarized('dark')[0], _ctx)

size(400, 300)
background(bg_color)

x = 67
y = 206

_scale = 37 * 0.01
line_height = 0 * _scale * 10
column_width = 0 * _scale * 10

project = 'Quantica'
gstring = '/g'

wts = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
wds = [ 5 ]

res = 4
alpha_ = make_alpha(res)

_color = RGB_to_nodebox_color(solarized('yellow'), _ctx, alpha=alpha_)

p = hProject(project)
_y = y
for wt in range(1, len(wts) + 1, res):
    wd = 5
    _style_name = '%s%s' % (wt, wd)
    ufo_path = p.fonts[_style_name]
    L = hLine(RFont(ufo_path), _ctx)
    L.txt(gstring, mode='gstring')
    L.draw((x, _y), scale_=_scale, color_=_color)
    _y += line_height
    x += column_width   
