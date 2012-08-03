# [h] print selected glyphs

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import print_selected_glyphs

font = CurrentFont()
print_selected_glyphs(font, mode=0)
