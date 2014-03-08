# dialogs.font

'''A collection of dialogs to do things to the current font.'''

# import

from adjust_vmetrics import adjustVerticalMetrics
from copy_info import copyFontInfoDialog
from create_spaces import createSpaceGlyphsDialog
from delete_layer import deleteLayerDialog
from import_layer import importUFOIntoLayerDialog
from print_groups import printGroupsDialog
from print_info import clearFontInfoDialog
from rename_glyphs import batchRenameGlyphs
from set_element import setElementDialog
from transfer_vmetrics import transferVMetricsDialog

# export

__all__ = [
    'adjustVerticalMetrics',
    'copyFontInfoDialog',
    'createSpaceGlyphsDialog',
    'deleteLayerDialog',
    'importUFOIntoLayerDialog',
    'printGroupsDialog',
	'clearFontInfoDialog',
    'batchRenameGlyphs',
    'setElementDialog',
    'transferVMetricsDialog',
]
