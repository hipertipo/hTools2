# [h] paint and arrange groups

'''Paint each group of glyphs in the font with a different color.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.color
    reload(hTools2.modules.color)

# import

from hTools2.modules.color import paint_groups

# run

f = CurrentFont()
paint_groups(f)
