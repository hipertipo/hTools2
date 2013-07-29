# [h] set width dialog

'''Set the advance width of the selected glyphs.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import setWidthDialog

# run

setWidthDialog()
