# [h] copy glyphs to mask

'''Copy selected glyphs from and to the mask layer.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import maskDialog

# run

maskDialog()
