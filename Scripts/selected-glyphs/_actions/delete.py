# [h] remove selected glyphs

'delete selected glyphs in font'

from hTools2.modules.fontutils import get_glyphs

f = CurrentFont()
glyph_names = get_glyphs(f)

for glyph_name in glyph_names:
    f.removeGlyph(glyph_name)
    if glyph_name in f.glyphOrder:
        f.glyphOrder.remove(glyph_name)

f.update()
