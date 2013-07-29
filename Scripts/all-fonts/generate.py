# [h] genenerate all open fonts

'''Genenerate otfs for all open fonts.'''

# debug

import hTools2.dialogs
reload(hTools2.dialogs)

if hTools2.DEBUG:
    import hTools2.dialogs.all_fonts
    reload(hTools2.dialogs.all_fonts)

# imports

from hTools2.dialogs.all_fonts import generateAllFontsDialog

# run

generateAllFontsDialog()
