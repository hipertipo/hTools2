# [h] draw glyph from ufo

from robofab.objects.objectsRF import RFont

from hTools2.objects import hGlyph, hLine

size(600, 400)
background(0)

x = 104
y = 204
s = 91 * 0.001

ufo_path = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_Guarana/_ufos/Guarana_15.ufo"
ufo = RFont(ufo_path)

L = hLine(ufo, _ctx)
L.txt('hipertipo')
L.draw((x, y),
       scale_=s,
       anchors=True,
       hmetrics=False,
       hmetrics_crop=False,
       origin=False,
       baseline=False)
