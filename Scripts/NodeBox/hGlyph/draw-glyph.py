# [h] draw glyph from ufo

from robofab.objects.objectsRF import RFont

from hTools2.objects import hGlyph_NodeBox

size(600, 400)
background(.3)

fill(1)

x = 171
y = 268

_scale = 25

ufo_path = u"/fonts/_Publica/_ufos/Publica_55.ufo"
ufo = RFont(ufo_path)

g = hGlyph_NodeBox(ufo['thorn'])
g.draw((x, y),
       _ctx,
       scale_=_scale / 100.00,
       baseline=True,
       margin=True,
       origin=True,
       vmetrics=True)
