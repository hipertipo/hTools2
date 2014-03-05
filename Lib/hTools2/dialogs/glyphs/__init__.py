#!/usr/bin/python
# -*- coding: utf-8 -*-

# [h] dialogs.glyphs

'''A collection of dialogs to do things to the selected glyphs of one or more fonts.'''

# import

from actions import glyphActionsDialog
from change_suffix import changeSuffixDialog
from copy_margins import copyMarginsDialog
from copy_to_layer import copyToLayerDialog
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
from set_margins import setMarginsDialog
from set_width import setWidthDialog
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
