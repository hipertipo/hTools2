# [h] print selected glyphs

'''Print the names of the selected glyphs as plain text or Python list..'''

# debug

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

# settings

# mode=0 : list of Python strings
# mode=1 : plain list with linebreaks

_mode = 0

# run

font = CurrentFont()
print_selected_glyphs(font, mode=_mode)
