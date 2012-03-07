# [h] draw ufo

from robofab.objects.objectsRF import RFont

from hTools2.objects import hGlyph, hLine

size(800, 600)
background(0)

x = 94
y = 326

_scale = 113 * 0.001
_color = color(0, 1, 0)

ufo_path = u"/fonts/_Publica/_ufos/Publica_55.ufo"
ufo = RFont(ufo_path)

_text = 'hello world'

L = hLine(ufo, _ctx)
L.txt(_text, mode='text')
L.draw((x, y),
       scale_=_scale,
       anchors=False,
       hmetrics=False,
       hmetrics_crop=False,
       origin=False,
       baseline=False,
       color_=_color)
