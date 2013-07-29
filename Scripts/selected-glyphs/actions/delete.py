# [h] remove selected glyphs

'''Remove selected glyphs from the current font.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# import

from hTools2.modules.fontutils import get_glyphs

# run

f = CurrentFont()
for glyph_name in get_glyphs(f):
    f.removeGlyph(glyph_name)
    if glyph_name in f.glyphOrder:
        f.glyphOrder.remove(glyph_name)
f.update()
