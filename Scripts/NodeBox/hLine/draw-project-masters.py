# [h] draw ufos

from robofab.objects.objectsRF import RFont

from hTools2.objects import hProject, hGlyph, hLine

size(1280, 800)
background(.1)

x = 53
y = 176

scale_ = 132 * 0.001
line_height = 123 * scale_ * 10

p = hProject('Publica')

for ufo_path in p.masters():
    L = hLine(RFont(ufo_path), _ctx)
    L.txt('handgloves', mode='text')
    L.draw((x, y),
           scale_=scale_,
           anchors=False,
           hmetrics=False,
           hmetrics_crop=False,
           origin=False,
           baseline=False)
    y += line_height
