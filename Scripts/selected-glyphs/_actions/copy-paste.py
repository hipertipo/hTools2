# [h] copy / paste

'''Copy glyph data and paste it into selected glyphs.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import copyPasteGlyphDialog

# run

copyPasteGlyphDialog()
