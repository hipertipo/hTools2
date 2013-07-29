# [h] genenerate all open fonts

'''Genenerate otfs for all open fonts.'''

# debug

import hTools2.dialogs
reload(hTools2.dialogs)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# imports

from hTools2.dialogs import generateAllFontsDialog

# run

generateAllFontsDialog()
