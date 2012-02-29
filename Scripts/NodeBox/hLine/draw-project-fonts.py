# [h] draw hProjects

colors = ximport("colors")

from robofab.objects.objectsRF import RFont

from hTools2.objects import hProject, hGlyph, hLine
from hTools2.modules.color import RGB_to_nodebox_color, solarized

bg_color = color(0)

size(1600, 1200)
background(bg_color)

_scale = 135 * 0.001
line_height = 89 * _scale * 10
column_width = 69 * _scale * 10
_text = 'nsnanhn'
_text_mode = 'text'

x = 36 * _scale * 10
y = 95 * _scale * 10

projects = [ 'Jornalistica' ]

wts = [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ]
wds = [ 5 ]
res = 2

color_step = 1.0 / len(range(1, len(wts) + 1, res))

for i in range(len(projects)):
    project_name = projects[i]
    p = hProject(project_name)
    _y = y
    _wt_count = 0
    for wt in range(1, len(wts) + 1, res):
        _color = colors.hsb(color_step * _wt_count, 1, 1)
        for wd in wds:
            _style_name = '%s%s' % (wt, wd)
            ufo_path = p.fonts[_style_name]
            fill(.3)
            font('EMono', 13)
            text('%s' % (_style_name), x, _y + 15)
            L = hLine(RFont(ufo_path), _ctx)
            L.txt(_text, mode= _text_mode)
            L.draw((x, _y), scale_=_scale, color_=_color)
            _y += line_height
        _wt_count += 1
    _y = y
    x += column_width
