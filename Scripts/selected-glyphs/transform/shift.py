# [h] shift points

'''Select points by position and shift them by a given distance.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import shiftPointsDialog

# run

shiftPointsDialog()
