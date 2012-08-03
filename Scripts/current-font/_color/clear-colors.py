# [h] clear colors

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.color
    reload(hTools2.modules.color)

from hTools2.modules.color import clear_colors

f = CurrentFont()
clear_colors(f)
