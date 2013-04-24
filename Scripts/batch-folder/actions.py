# [h] apply actions

'''Batch apply actions to all fonts in folder.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# imports

from hTools2.dialogs import actionsFolderDialog

# run

actionsFolderDialog()
