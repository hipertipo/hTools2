# [h] nudge selected points

'''Nudge selected points by a given amount of units, with differents modes possible.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyph
    reload(hTools2.dialogs.glyph)

# import

from hTools2.dialogs.glyph import nudgePointsDialog

# run

nudgePointsDialog()
