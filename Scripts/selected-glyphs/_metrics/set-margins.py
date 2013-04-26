# [h] set margins dialog

'''Set left/right side-bearings of selected glyphs.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import setMarginsDialog

# run

setMarginsDialog()
