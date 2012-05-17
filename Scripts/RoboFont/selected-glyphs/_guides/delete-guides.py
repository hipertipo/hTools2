# [h] clear guides

from hTools2.modules.glyphutils import *
from hTools2.modules.fontutils import get_glyphs

f = CurrentFont()

for glyph_name in get_glyphs(f):
    clear_guides(f[glyph_name])
    f[glyph_name].update()