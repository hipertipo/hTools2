# [h] copy glyphs to mask

'''Copy selected glyphs from and to the mask layer.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import maskDialog

# run

maskDialog()
