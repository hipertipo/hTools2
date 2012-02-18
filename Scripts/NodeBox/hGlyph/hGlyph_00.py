# [h] draw glyph from ufo

from robofab.objects.objectsRF import RFont

import hTools2.objects
reload(hTools2.objects)

from hTools2.objects import hGlyph

size(600, 400)
background(.5)

fill(1)

x = 166
y = 248

_scale = 23

ufo_path = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_Publica/_ufos/Publica_55.ufo"
ufo = RFont(ufo_path)

glyph = hGlyph(ufo['thorn'])
glyph.draw((x, y),
        _ctx,
        scale_=_scale/100.00,
        baseline=True,
        margin=True,
        origin=True,
        vmetrics=True)
