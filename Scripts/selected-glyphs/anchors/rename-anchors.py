# [h] rename anchors

'''Change the name of anchors in selected glyphs into a new name.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# imports

from hTools2.dialogs.glyphs import renameAnchorsDialog

# run

renameAnchorsDialog()
