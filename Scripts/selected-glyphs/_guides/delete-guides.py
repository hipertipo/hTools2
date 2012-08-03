# [h] clear guides

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.glyphutils
    reload(hTools2.modules.glyphutils)

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

from hTools2.modules.glyphutils import clear_guides
from hTools2.modules.fontutils import get_glyphs

f = CurrentFont()

for glyph_name in get_glyphs(f):
    clear_guides(f[glyph_name])
    f[glyph_name].update()
