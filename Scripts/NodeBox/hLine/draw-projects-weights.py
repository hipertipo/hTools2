# [h] draw hProjects, superimpose weights

from robofab.objects.objectsRF import RFont

from hTools2.objects import hProject, hGlyph, hLine
from hTools2.modules.color import *
from hTools2.modules.nodebox import make_alpha

bg_color = color(0) # RGB_to_nodebox_color(solarized('dark')[0], _ctx)

size(960, 720)
background(bg_color)

_scale = 150 * 0.001
line_height = 90 * _scale * 10
column_width = 80 * _scale * 10
gstrings = [ '/d', '/a', '/n', '/g' ]
projects = [
    'Magnetica',
    'Mechanica',
    'Guarana',
    'Quantica',
    'Synthetica',
    'Publica',
    'Jornalistica'
]
wts = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
wds = [ 5 ]

res = 2
alpha_ = make_alpha(res)
subtext = False

x = 60
y = 190

for i in range(len(projects)):
    _color = RGB_to_nodebox_color(solarized('colors')[i], _ctx, alpha=alpha_)
    project_name = projects[i]
    p = hProject(project_name)
    _y = y
    for wt in range(1, len(wts) + 1, res):
        for wd in wds:
            _style_name = '%s%s' % (wt, wd)
            ufo_path = p.fonts[_style_name]
            for gstring in gstrings:
                L = hLine(RFont(ufo_path), _ctx)
                L.txt(gstring, mode='gstring')
                L.draw((x, _y), scale_=_scale, color_=_color)
                _y += line_height
        _y = y
    x += column_width
