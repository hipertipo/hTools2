# [h] print selected glyphs

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# import

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import print_selected_glyphs

# run

font = CurrentFont()
print_selected_glyphs(font, mode=0)
