#!/usr/bin/python
# -*- coding: utf-8 -*-

# [h] dialogs.glyphs

"""A collection of dialogs to do things to the selected glyphs of one or more fonts."""

# import

from actions import glyphActionsDialog
from anchors_move import moveAnchorsDialog
from anchors_rename import renameAnchorsDialog
from anchors_transfer import transferAnchorsDialog
from copy_paste import copyPasteGlyphDialog
from elements_rasterize import rasterizeGlyphDialog
from elements_randomize import randomizeElementsDialog
from gridfit import roundToGridDialog
from interpolate import interpolateGlyphsDialog
from interpolate_check import checkGlyphsCompatibilityDialog
from interpolate_condense import condenseGlyphsDialog
# from layers_align import alignLayersDialog
from layers_copy import copyToLayerDialog
from margins_copy import copyMarginsDialog
from margins_set import setMarginsDialog
from mask import maskDialog
from mask_copy import copyToMaskDialog
from mirror import mirrorGlyphsDialog
from move import moveGlyphsDialog
from names_print import printGlyphsDialog
from names_suffix import changeSuffixDialog
from outline import outlineGlyphsDialog
from paint_select import paintGlyphsDialog
from points_shift import shiftPointsDialog
from scale import scaleGlyphsDialog
from skew import skewGlyphsDialog
from slide import slideGlyphsDialog
from width_copy import copyWidthsDialog
from width_set import setWidthDialog

# export

__all__ = [
    'glyphActionsDialog',
    'moveAnchorsDialog',
    'renameAnchorsDialog',
    'transferAnchorsDialog',
    'copyPasteGlyphDialog',
    'roundToGridDialog',
    'interpolateGlyphsDialog',
    'checkGlyphsCompatibilityDialog',
    'condenseGlyphsDialog',
    # 'alignLayersDialog',
    'copyToLayerDialog',
    'copyMarginsDialog',
    'setMarginsDialog',
    'maskDialog',
    'copyToMaskDialog',
    'mirrorGlyphsDialog',
    'moveGlyphsDialog',
    'printGlyphsDialog',
    'changeSuffixDialog',
    'outlineGlyphsDialog',
    'paintGlyphsDialog',
    'shiftPointsDialog',
    'rasterizeGlyphDialog',
    'randomizeElementsDialog',
    'scaleGlyphsDialog',
    'skewGlyphsDialog',
    'slideGlyphsDialog',
    'copyWidthsDialog',
    'setWidthDialog',
]
