# [h] paint and select

'''Paint selected glyphs and select glyphs by color.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import paintGlyphsDialog

# run

paintGlyphsDialog()
