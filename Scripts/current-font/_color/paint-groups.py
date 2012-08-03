# [h] paint and arrange groups

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.color
    reload(hTools2.modules.color)

from hTools2.modules.color import paint_groups

# run

f = CurrentFont()
paint_groups(f)
