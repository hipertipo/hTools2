# [h] dialogs.glyph

"""A collection of dialogs to do things to the current glyph."""

import align
reload(align)

import nudge
reload(nudge)

import switch
reload(switch)

import interpolation_preview
reload(interpolation_preview)

# import

from align import alignPointsDialog
from nudge import nudgePointsDialog
from switch import switchGlyphDialog
from interpolation_preview import interpolationPreviewDialog

# export

__all__ = [
    'alignPointsDialog',
    'nudgePointsDialog',
    'switchGlyphDialog',
    'interpolationPreviewDialog',
]
