# [h] convert otfs to ufos

'''Convert all otf fonts in a folder into ufos.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# imports

from hTools2.dialogs import OTFsToUFOsDialog

# run

OTFsToUFOsDialog()
