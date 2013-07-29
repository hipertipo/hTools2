# [h] actions

'''Apply common actions to selected glyphs.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# imports

from hTools2.dialogs import glyphActionsDialog

# run

glyphActionsDialog()
