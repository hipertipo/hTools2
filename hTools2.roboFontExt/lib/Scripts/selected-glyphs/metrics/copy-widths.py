# [h] copy widths dialog

'''Copy the advance widths in selected glyphs from one font to another.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import copyWidthsDialog

# run

copyWidthsDialog()
