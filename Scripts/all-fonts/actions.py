# [h] transform all open fonts

'''Apply selected actions to all open fonts.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.all_fonts
    reload(hTools2.dialogs.all_fonts)

# import

from hTools2.dialogs.all_fonts import actionsDialog

# run

actionsDialog()
