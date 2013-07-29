# [h] dialogs.glyphs

'''A collection of dialogs to do things to the selected glyphs of one or more fonts.'''

import hTools2
reload(hTools2)

# debug

if hTools2.DEBUG:

    import actions
    reload(actions)

    import change_suffix
    reload(change_suffix)

    import copy_margins
    reload(copy_margins)

    import copy_paste
    reload(copy_paste)

    import copy_to_mask
    reload(copy_to_mask)

    import copy_to_layer
    reload(copy_to_layer)

    import copy_widths
    reload(copy_widths)

    import interpolate
    reload(interpolate)

    import mask
    reload(mask)

    import mirror
    reload(mirror)

    import move
    reload(move)

    import move_anchors
    reload(move_anchors)

    import rasterize
    reload(rasterize)

    import round_to_grid
    reload(round_to_grid)

    import set_width
    reload(set_width)

    import set_margins
    reload(set_margins)

    import shift_points
    reload(shift_points)

    import scale
    reload(scale)

    import skew
    reload(skew)

    import slide
    reload(slide)

    import paint
    reload(paint)

    import rename_anchors
    reload(rename_anchors)

    import transfer_anchors
    reload(transfer_anchors)

# import

from actions import glyphActionsDialog
from change_suffix import changeSuffixDialog
from copy_to_layer import copyToLayerDialog
from copy_margins import copyMarginsDialog
from copy_to_mask import copyToMaskDialog
from copy_paste import copyPasteGlyphDialog
from copy_widths import copyWidthsDialog
from interpolate import interpolateGlyphsDialog
from mask import maskDialog
from mirror import mirrorGlyphsDialog
from move import moveGlyphsDialog
from move_anchors import moveAnchorsDialog
from paint import paintGlyphsDialog
from rasterize import rasterizeGlyphDialog
from rename_anchors import renameAnchorsDialog
from round_to_grid import roundToGridDialog
from scale import scaleGlyphsDialog
from set_width import setWidthDialog
from set_margins import setMarginsDialog
from shift_points import shiftPointsDialog
from skew import skewGlyphsDialog
from slide import slideGlyphsDialog
from transfer_anchors import transferAnchorsDialog

# export

__all__ = [
    'copyMarginsDialog',
    'copyWidthsDialog',
    'copyToMaskDialog',
    'changeSuffixDialog',
    'moveAnchorsDialog',
    'moveGlyphsDialog',
    'maskDialog',
    'copyToLayerDialog',
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
]
