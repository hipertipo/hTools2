# [h] import ufo into layer

'''Import font from ufo into layer.'''

# reload

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import importUFOIntoLayerDialog

# run

importUFOIntoLayerDialog()
