# [h] dialogs.glyph

"""A collection of dialogs to do things to the current glyph."""

# debug

import align
reload(align)

import nudge
reload(nudge)

import switch
reload(switch)

# import

from align import alignPointsDialog
from nudge import nudgePointsDialog
from switch import switchGlyphDialog

# export

__all__ = [
    'alignPointsDialog',
    'nudgePointsDialog',
    'switchGlyphDialog',
]
