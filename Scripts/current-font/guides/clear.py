# [h] clear font guides

'''Remove all global guides in the font.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# imports

from hTools2.modules.fontutils import get_glyphs, clear_guides

# run

f = CurrentFont()
clear_guides(f)
