# [h] convert woffs to ufos

'''Convert all woffs in a folder into ufos.'''

# debug

import hTools2.dialogs.folder
reload(hTools2.dialogs.folder)

# imports

from hTools2.dialogs.folder import WOFFsToUFOsDialog

# run

WOFFsToUFOsDialog()
