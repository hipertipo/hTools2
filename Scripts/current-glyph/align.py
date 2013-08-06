# [h] align selected points

'''Align selected points vertically or horizontally.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyph
    reload(hTools2.dialogs.glyph)

# import

from hTools2.dialogs.glyph import alignPointsDialog

# run

alignPointsDialog()
