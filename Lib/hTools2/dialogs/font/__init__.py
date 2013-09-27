# dialogs.font

'''A collection of dialogs to do things to the current font.'''

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
