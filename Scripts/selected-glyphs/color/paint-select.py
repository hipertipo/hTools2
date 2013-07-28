# [h] paint and select

'''Paint selected glyphs and select glyphs by color.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import paintGlyphsDialog

# run

paintGlyphsDialog()
