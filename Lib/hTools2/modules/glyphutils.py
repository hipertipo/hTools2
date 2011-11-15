# [h] hTools2.modules.glyphutils

def centerGlyph(glyph):
    whitespace = glyph.leftMargin + glyph.rightMargin
    glyph.leftMargin = whitespace / 2
    glyph.rightMargin = whitespace / 2
