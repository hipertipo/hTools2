'''dialogs'''

import hTools2
reload(hTools2)

#-----------------------
# reload when debugging
#-----------------------

if hTools2.DEBUG:

    import glyphs_copy_to_mask
    reload(glyphs_copy_to_mask)

    import glyphs_mask
    reload(glyphs_mask)

    import glyphs_copy_to_layer
    reload(glyphs_copy_to_layer)

    import glyphs_mirror
    reload(glyphs_mirror)

    import glyphs_copy_paste
    reload(glyphs_copy_paste)

    import glyphs_round_to_grid
    reload(glyphs_round_to_grid)

    import glyphs_shift_points
    reload(glyphs_shift_points)

    import glyphs_move
    reload(glyphs_move)

    import glyphs_scale
    reload(glyphs_scale)

    import glyphs_skew
    reload(glyphs_skew)

    import glyphs_rasterize
    reload(glyphs_rasterize)

    import glyphs_actions
    reload(glyphs_actions)

    import glyphs_set_width
    reload(glyphs_set_width)

    import glyphs_set_margins
    reload(glyphs_set_margins)

    import glyphs_copy_margins
    reload(glyphs_copy_margins)

    import glyphs_interpolate
    reload(glyphs_interpolate)

    import glyphs_paint
    reload(glyphs_paint)

    import glyphs_move_anchors
    reload(glyphs_move_anchors)

    import glyphs_rename_anchors
    reload(glyphs_rename_anchors)

    import glyphs_transfer_anchors
    reload(glyphs_transfer_anchors)

    import glyphs_change_suffix
    reload(glyphs_change_suffix)

    import folder_actions
    reload(folder_actions)

    import folder_generate
    reload(folder_generate)

    import folder_otfs2ufos
    reload(folder_otfs2ufos)

#----------------
# import dialogs
#----------------

from glyphs_copy_to_mask import copyToMaskDialog
from glyphs_mask import maskDialog
from glyphs_copy_to_layer import copyToLayer

from glyphs_mirror import mirrorGlyphsDialog
from glyphs_copy_paste import copyPasteGlyphDialog
from glyphs_round_to_grid import roundToGridDialog
from glyphs_shift_points import shiftPointsDialog
from glyphs_move import moveGlyphsDialog
from glyphs_scale import scaleGlyphsDialog
from glyphs_skew import skewGlyphsDialog
from glyphs_rasterize import rasterizeGlyphDialog
from glyphs_actions import glyphActionsDialog

from glyphs_set_width import setWidthDialog
from glyphs_set_margins import setMarginsDialog
from glyphs_copy_margins import copyMarginsDialog

from glyphs_interpolate import interpolateGlyphsDialog

from glyphs_paint import paintGlyphsDialog

from glyphs_move_anchors import moveAnchorsDialog
from glyphs_rename_anchors import renameAnchorsDialog
from glyphs_transfer_anchors import transferAnchorsDialog
from glyphs_change_suffix import changeSuffixDialog

from folder_actions import actionsFolderDialog
from folder_generate import generateFolderDialog
from folder_otfs2ufos import OTFsToUFOsDialog

#----------------
# export dialogs
#----------------

selected_glyphs = [
    # layers
    'copyToMaskDialog',
    'maskDialog',
    'copyToLayer',
    'mirrorGlyphsDialog',
    'copyPasteGlyphDialog',
    'roundToGridDialog',
    'shiftPointsDialog',
    'moveGlyphsDialog',
    'scaleGlyphsDialog',
    'skewGlyphsDialog',
    'rasterizeGlyphDialog',
    'glyphActionsDialog',
    # spacing
    'setWidthDialog',
    'setMarginsDialog',
    'copyMarginsDialog',
    # interpolation
    'interpolateGlyphsDialog',
    # color
    'paintGlyphsDialog',
    # anchors
    'moveAnchorsDialog',
    'renameAnchorsDialog',
    'transferAnchorsDialog',
    # glyph names
    'changeSuffixDialog',
]

batch_folder = [
    'OTFsToUFOsDialog',
    'generateFolderDialog',
    'actionsFolderDialog',
]

__all__ = selected_glyphs + batch_folder
