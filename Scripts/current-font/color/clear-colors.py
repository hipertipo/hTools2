# [h] clear colors

'''Clear colors of all glyphs in font.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.color
    reload(hTools2.modules.color)

# import

from hTools2.modules.color import clear_colors

# run

f = CurrentFont()
clear_colors(f)
