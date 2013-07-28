# [h] import ufo into layer

'''Import font from ufo into layer.'''

# reload

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.font
    reload(hTools2.dialogs.font)

# import

from hTools2.dialogs.font import importUFOIntoLayerDialog

# run

importUFOIntoLayerDialog()
