#FLM: [h] get glyphs test

from robofab.world import CurrentFont

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print gNames
