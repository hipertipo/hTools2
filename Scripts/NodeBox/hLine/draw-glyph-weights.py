# [h] draw hProject glyph weights

from robofab.objects.objectsRF import RFont

from hTools2.objects import hProject, hGlyph, hLine
from hTools2.modules.color import RGB_to_nodebox_color, solarized
from hTools2.modules.nodebox import make_alpha

size(1280, 800)
background(0)

x = 108
y = 509

_scale = 65 * 0.01
line_height = 0 * _scale * 10
column_width = 60 * _scale * 10

project = 'Publica'
gstring = '/e'

wts = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
wds = [ 5 ]
res = 2

# draw

p = hProject(project)
_y = y
glyphs = gstring.split('/')
alpha_ = make_alpha(res)
_color = RGB_to_nodebox_color(solarized('cyan'), _ctx, alpha=alpha_)

for glyph in glyphs:
    if glyph is not '':
        glyph_name = '/%s' % glyph
        for wt in range(1, len(wts) + 1, res):
            wd = 5
            _style_name = '%s%s' % (wt, wd)
            ufo_path = p.fonts[_style_name]
            L = hLine(RFont(ufo_path), _ctx)
            L.txt(glyph_name, mode='gstring')
            L.draw((x, _y), scale_=_scale, color_=_color)
            _y += line_height
        x += column_width   
