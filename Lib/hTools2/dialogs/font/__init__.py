# dialogs.font

"""A collection of dialogs to do things to the current font."""

# import

from element_set import setElementDialog
from groups_print import printGroupsDialog
from glyphs_rename import batchRenameGlyphs
from info_copy import copyFontInfoDialog
from info_print import clearFontInfoDialog
from layer_delete import deleteLayerDialog
from layer_import import importUFOIntoLayerDialog
from spaces_create import createSpaceGlyphsDialog
from vmetrics_adjust import adjustVerticalMetrics
from vmetrics_transfer import transferVMetricsDialog

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
