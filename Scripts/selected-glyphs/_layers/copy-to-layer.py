# [h] copy to layer

'''Copy selected glyphs to a given layer.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import copyToLayerDialog

# run

copyToLayerDialog()
