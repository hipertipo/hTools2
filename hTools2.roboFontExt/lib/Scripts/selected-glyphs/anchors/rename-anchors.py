# [h] rename anchors

'''Change the name of anchors in selected glyphs into a new name.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# imports

from hTools2.dialogs import renameAnchorsDialog

# run

renameAnchorsDialog()
