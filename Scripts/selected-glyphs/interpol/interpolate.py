# [h] interpolate selected glyphs

'''Interpolate selected glyphs from one font with another into a third font.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import interpolateGlyphsDialog

# run

interpolateGlyphsDialog()
