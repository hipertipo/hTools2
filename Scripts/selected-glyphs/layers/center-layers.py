# [h] center layers

'''Center all layers in selected glyphs.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import alignLayersDialog

# run

alignLayersDialog()
