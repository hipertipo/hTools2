# [h] move glyphs dialog

'''Move contours in selected glyphs by a given distance.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import moveGlyphsDialog

# run

moveGlyphsDialog()
