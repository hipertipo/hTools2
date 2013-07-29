# [h] transfer anchors dialog

'''Transfer anchors in selected glyphs from one font to another.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# imports

from hTools2.dialogs.glyphs import transferAnchorsDialog

# run

transferAnchorsDialog()
