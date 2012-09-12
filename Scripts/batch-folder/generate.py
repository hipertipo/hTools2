# [h] batch generate otfs from folder

'''a dialog to genenerate otfs for all ufo fonts in a folder'''

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# imports

from hTools2.dialogs import generateFolderDialog

# run

generateFolderDialog()
