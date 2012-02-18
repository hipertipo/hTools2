# [h] draw a line of glyphs from ufos

from robofab.objects.objectsRF import RFont

from hTools2.objects import hProject, hGlyph, hLine

size(600, 600)
background(.1)

x = 53
y = 176

scale_ = 80 * 0.001
line_height = 123 * scale_ * 10

p = hProject('Synthetica')

for ufo_path in p.masters():
    L = hLine(RFont(ufo_path), _ctx)
    L.txt('/H/a/n/d/g.alt/l/o/v/e/s', mode='gstring')
    L.draw((x, y),
           scale_=scale_,
           anchors=False,
           hmetrics=False,
           hmetrics_crop=False,
           origin=False,
           baseline=False)
    y += line_height
