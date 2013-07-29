# dialogs.font

'''A collection of dialogs to do things to the current font.'''

import hTools2
reload(hTools2)

# debug

if hTools2.DEBUG:

    import adjust_vmetrics
    reload(adjust_vmetrics)

    import create_spaces
    reload(create_spaces)

    import delete_layer
    reload(delete_layer)

    import import_layer
    reload(import_layer)

    import print_groups
    reload(print_groups)

    import rename_glyphs
    reload(rename_glyphs)

    import transfer_vmetrics
    reload(transfer_vmetrics)

# import

from adjust_vmetrics import adjustVerticalMetrics
from create_spaces import createSpaceGlyphsDialog
from delete_layer import deleteLayerDialog
from import_layer import importUFOIntoLayerDialog
from print_groups import printGroupsDialog
from rename_glyphs import batchRenameGlyphs
from transfer_vmetrics import transferVMetricsDialog

# export

__all__ = [
    'batchRenameGlyphs',
    'createSpaceGlyphsDialog',
    'printGroupsDialog',
    'deleteLayerDialog',
    'importUFOIntoLayerDialog',
    'adjustVerticalMetrics',
    'transferVMetricsDialog',
]
