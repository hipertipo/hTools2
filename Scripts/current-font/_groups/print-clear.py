# [h] print groups in different formats

'''Print glyph groups as text in different formats.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import printGroupsDialog

# run

printGroupsDialog()
