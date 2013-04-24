# [h] set width dialog

'''Set the advance width of the selected glyphs.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import setWidthDialog

# run

setWidthDialog()
