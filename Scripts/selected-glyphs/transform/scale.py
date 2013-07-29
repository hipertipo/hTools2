# [h] scale glyphs dialog

'''Scale selected glyphs by a given factor.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import scaleGlyphsDialog

# run

scaleGlyphsDialog()
