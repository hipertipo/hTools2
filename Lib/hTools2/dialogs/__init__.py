'''dialogs'''

import hTools2
reload(hTools2)

# debug

if hTools2.DEBUG:

    # glyphs

    import glyphs_actions
    reload(glyphs_actions)

    import glyphs_change_suffix
    reload(glyphs_change_suffix)

    import glyphs_copy_margins
    reload(glyphs_copy_margins)

    import glyphs_copy_paste
    reload(glyphs_copy_paste)

    import glyphs_copy_to_mask
    reload(glyphs_copy_to_mask)

    import glyphs_copy_to_layer
    reload(glyphs_copy_to_layer)

    import glyphs_copy_widths
    reload(glyphs_copy_widths)

    import glyphs_interpolate
    reload(glyphs_interpolate)

    import glyphs_mask
    reload(glyphs_mask)

    import glyphs_mirror
    reload(glyphs_mirror)

    import glyphs_move
    reload(glyphs_move)

    import glyphs_move_anchors
    reload(glyphs_move_anchors)

    import glyphs_rasterize
    reload(glyphs_rasterize)

    import glyphs_round_to_grid
    reload(glyphs_round_to_grid)

    import glyphs_set_width
    reload(glyphs_set_width)

    import glyphs_set_margins
    reload(glyphs_set_margins)

    import glyphs_shift_points
    reload(glyphs_shift_points)

    import glyphs_skew
    reload(glyphs_skew)

    import glyphs_slide
    reload(glyphs_slide)

    import glyphs_paint
    reload(glyphs_paint)

    import glyphs_rename_anchors
    reload(glyphs_rename_anchors)

    import glyphs_transfer_anchors
    reload(glyphs_transfer_anchors)

    # folder

    import folder_actions
    reload(folder_actions)

    import folder_generate
    reload(folder_generate)

    import folder_otfs2ufos
    reload(folder_otfs2ufos)

    # font

    import font_adjust_vmetrics
    reload(font_adjust_vmetrics)

    import font_delete_layer
    reload(font_delete_layer)

    import font_create_spaces
    reload(font_create_spaces)

    import font_import_layer
    reload(font_import_layer)

    import font_print_groups
    reload(font_print_groups)

    import font_rename_glyphs
    reload(font_rename_glyphs)

    import font_transfer_vmetrics
    reload(font_transfer_vmetrics)

    # other

    import select_fonts
    reload(select_fonts)

# import dialogs

from folder_actions import actionsFolderDialog
from folder_generate import generateFolderDialog
from folder_otfs2ufos import OTFsToUFOsDialog

from font_adjust_vmetrics import adjustVerticalMetrics
from font_create_spaces import createSpaceGlyphsDialog
from font_delete_layer import deleteLayerDialog
from font_import_layer import importUFOIntoLayerDialog
from font_print_groups import printGroupsDialog
from font_rename_glyphs import batchRenameGlyphs
from font_transfer_vmetrics import transferVMetricsDialog

from glyphs_actions import glyphActionsDialog
from glyphs_change_suffix import changeSuffixDialog
from glyphs_copy_to_layer import copyToLayerDialog
from glyphs_copy_margins import copyMarginsDialog
from glyphs_copy_to_mask import copyToMaskDialog
from glyphs_copy_paste import copyPasteGlyphDialog
from glyphs_copy_widths import copyWidthsDialog
from glyphs_interpolate import interpolateGlyphsDialog
from glyphs_mask import maskDialog
from glyphs_mirror import mirrorGlyphsDialog
from glyphs_move import moveGlyphsDialog
from glyphs_move_anchors import moveAnchorsDialog
from glyphs_paint import paintGlyphsDialog
from glyphs_rasterize import rasterizeGlyphDialog
from glyphs_rename_anchors import renameAnchorsDialog
from glyphs_round_to_grid import roundToGridDialog
from glyphs_scale import scaleGlyphsDialog
from glyphs_set_width import setWidthDialog
from glyphs_set_margins import setMarginsDialog
from glyphs_shift_points import shiftPointsDialog
from glyphs_skew import skewGlyphsDialog
from glyphs_slide import slideGlyphsDialog
from glyphs_transfer_anchors import transferAnchorsDialog

from select_fonts import SelectFonts

# export dialogs

__all__ = [
    # glyph
    'copyMarginsDialog',
    'copyWidthsDialog',
    'copyToMaskDialog',
    'changeSuffixDialog',
    'moveAnchorsDialog',
    'moveGlyphsDialog',
    'maskDialog',
    'copyToLayer',
    'copyPasteGlyphDialog',
    'mirrorGlyphsDialog',
    'glyphActionsDialog',
    'interpolateGlyphsDialog',
    'paintGlyphsDialog',
    'rasterizeGlyphDialog',
    'renameAnchorsDialog',
    'roundToGridDialog',
    'shiftPointsDialog',
    'scaleGlyphsDialog',
    'skewGlyphsDialog',
    'slideGlyphsDialog',
    'setWidthDialog',
    'setMarginsDialog',
    'transferAnchorsDialog',
    # folder
    'actionsFolderDialog',
    'OTFsToUFOsDialog',
    'generateFolderDialog',
    # font
    'batchRenameGlyphs',
    'createSpaceGlyphsDialog',
    'printGroupsDialog',
    'deleteLayerDialog',
    'importUFOIntoLayerDialog',
    'adjustVerticalMetrics',
    'transferVMetricsDialog',
    # other
    'SelectFonts',
]
