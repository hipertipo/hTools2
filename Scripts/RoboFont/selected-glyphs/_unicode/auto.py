# [h] auto unicodes

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.encoding import auto_unicode

f = CurrentFont()

glyph_names = get_glyphs(f)

for glyph_name in glyph_names:
    auto_unicode(f[glyph_name])
    