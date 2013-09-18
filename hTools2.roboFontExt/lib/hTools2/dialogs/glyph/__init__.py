# [h] dialogs.glyph

'''A collection of dialogs to do things to the current glyph.'''

import hTools2
reload(hTools2)

# debug

if hTools2.DEBUG:

    import align_points
    reload(align_points)

    import nudge_points
    reload(nudge_points)

    import switch_glyph
    reload(switch_glyph)

# import

from align_points import alignPointsDialog
from nudge_points import nudgePointsDialog
from switch_glyph import switchGlyphDialog

# export

__all__ = [
    'alignPointsDialog',
    'nudgePointsDialog',
    'switchGlyphDialog',
]
