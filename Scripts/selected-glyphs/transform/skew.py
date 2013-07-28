# [h] skew glyphs dialog

'''Skew selected glyphs by a given angle.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# imports

from hTools2.dialogs.glyphs import skewGlyphsDialog

# run

skewGlyphsDialog()
