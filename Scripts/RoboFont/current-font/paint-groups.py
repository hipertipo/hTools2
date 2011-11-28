# [h] paing glyph groups

from hTools2.modules.colorsys import hls_to_rgb

def paintGroups(font):
    colorStep = 1.0 / len(f.groups)
    color = 0
    for group in f.groups.keys():
        _r, _g, _b = hls_to_rgb(color, 0.7, 1.0)
        for glyphName in f.groups[group]:
            if font.has_key(glyphName) != True:
                font.newGlyph(glyphName)
                font.update()
            font[glyphName].mark = (_r, _g, _b, 1)
            font[glyphName].update()
        color = color + colorStep
        if color > 1:
            color = color - 1
    font.update()

f = CurrentFont()
paintGroups(f)
