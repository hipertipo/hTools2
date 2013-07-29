# [h] batch generate otfs from folder

'''Genenerate .otfs for all .ufo fonts in a folder.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.folder
    reload(hTools2.dialogs.folder)

# imports

from hTools2.dialogs.folder import generateFolderDialog

# run

generateFolderDialog()
