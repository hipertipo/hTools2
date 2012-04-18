from hTools2.objects import hProject

p = hProject('Gothica')

for font in p.fonts:
    ufo = RFont(p.fonts[font], showUI=False)
    ufo.kerning.clear()
    print len(ufo.kerning)
    ufo.save()