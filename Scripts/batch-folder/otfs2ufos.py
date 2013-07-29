# [h] convert otfs to ufos

'''Convert all otf fonts in a folder into ufos.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.folder
    reload(hTools2.dialogs.folder)

# imports

from hTools2.dialogs.folder import OTFsToUFOsDialog

# run

OTFsToUFOsDialog()
