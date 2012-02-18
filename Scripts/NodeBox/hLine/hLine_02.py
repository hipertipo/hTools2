# [h] draw a line of glyphs from ufos

from robofab.objects.objectsRF import RFont

from hTools2.objects import hProject, hGlyph, hLine
from hTools2.modules.color import RGB_to_nodebox_color, solarized

bg_color = color(0) # RGB_to_nodebox_color(solarized('dark')[0], _ctx)

size(800, 600)
background(bg_color)

x = 50
y = 170

_scale = 140 * 0.001
line_height = 110 * _scale * 10
column_width = 75 * _scale * 10
gstring = '/c'

projects = [ 'Magnetica', 'Mechanica', 'Guarana', 'Quantica', \
            'Publica', 'Synthetica', 'Jornalistica', ]

wts = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
wds = [ 5 ]

res = 4

for i in range(len(projects)):
    _color = RGB_to_nodebox_color(solarized('colors')[i], _ctx)
    project_name = projects[i]
    p = hProject(project_name)
    _y = y
    for wt in range(1, len(wts) + 1, res):
        for wd in wds:
            _style_name = '%s%s' % (wt, wd)
            ufo_path = p.fonts[_style_name]
            L = hLine(RFont(ufo_path), _ctx)
            L.txt(gstring, mode='gstring')
            L.draw((x, _y), scale_=_scale, color_=_color)
            font('EMono', 13)
            text('%s' % (_style_name), x, _y + 15)
            _y += line_height
    _y = y
    x += column_width
