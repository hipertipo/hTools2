'''dialogs'''

DEBUG = True

# layers

if DEBUG:
    import copy_to_mask
    reload(copy_to_mask)
from copy_to_mask import copyToMaskDialog

if DEBUG:
    import mask_dialog
    reload(mask_dialog)
from mask_dialog import maskDialog

if DEBUG:
    import copy_to_layer
    reload(copy_to_layer)
from copy_to_layer import copyToLayer

# transformation

if DEBUG:
    import mirror_glyphs
    reload(mirror_glyphs)
from mirror_glyphs import mirrorGlyphsDialog

if DEBUG:
    import copy_paste_glyphs
    reload(copy_paste_glyphs)
from copy_paste_glyphs import copyPasteGlyphDialog

if DEBUG:
    import round_to_grid
    reload(round_to_grid)
from round_to_grid import roundToGridDialog

if DEBUG:
    import shift_points
    reload(shift_points)
from shift_points import shiftPointsDialog

if DEBUG:
    import move_glyphs
    reload(move_glyphs)
from move_glyphs import moveGlyphsDialog

if DEBUG:
    import scale_glyphs
    reload(scale_glyphs)
from scale_glyphs import scaleGlyphsDialog

if DEBUG:
    import skew_glyphs
    reload(skew_glyphs)
from skew_glyphs import skewGlyphsDialog

if DEBUG:
    import rasterize_glyphs
    reload(rasterize_glyphs)
from rasterize_glyphs import rasterizeGlyphDialog

if DEBUG:
    import glyph_actions
    reload(glyph_actions)
from glyph_actions import glyphActionsDialog

# spacing

if DEBUG:
    import set_glyph_width
    reload(set_glyph_width)
from set_glyph_width import setWidthDialog

if DEBUG:
    import set_margins
    reload(set_margins)
from set_margins import setMarginsDialog

if DEBUG:
    import copy_margins
    reload(copy_margins)
from copy_margins import copyMarginsDialog

# interpolation

if DEBUG:
    import interpolate_glyphs
    reload(interpolate_glyphs)
from interpolate_glyphs import interpolateGlyphsDialog

# color

if DEBUG:
    import paint_glyphs
    reload(paint_glyphs)
from paint_glyphs import paintGlyphsDialog

# anchors

if DEBUG:
    import move_anchors
    reload(move_anchors)
from move_anchors import moveAnchorsDialog

if DEBUG:
    import rename_anchors
    reload(rename_anchors)
from rename_anchors import renameAnchorsDialog

if DEBUG:
    import transfer_anchors
    reload(transfer_anchors)
from transfer_anchors import transferAnchorsDialog

if DEBUG:
    import change_suffix
    reload(change_suffix)
from change_suffix import changeSuffixDialog

# wrap dialogs

__all__ = [
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
