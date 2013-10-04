# [h] remove selected glyphs

f = CurrentFont()
for glyph_name in f.selection:
    f.removeGlyph(glyph_name)
    if glyph_name in f.glyphOrder:
        f.glyphOrder.remove(glyph_name)
f.update()
