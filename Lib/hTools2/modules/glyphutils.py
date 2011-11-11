# [h] hTools2.modules.glyphutils

def decompose(f):
	for g in f:
		g.decompose()

def autoContourOrderDirection(f):
	for g in f:
		g.autoContourOrder()
		g.correctDirection()

def centerGlyph(glyph):
    whitespace = glyph.leftMargin + glyph.rightMargin
    glyph.leftMargin = whitespace / 2
    glyph.rightMargin = whitespace / 2
