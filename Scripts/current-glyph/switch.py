# [h] switch current glyph

'''Switch the contents of the current glyph window (layers, glyphs, fonts).'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyph
    reload(hTools2.dialogs.glyph)

# import

from hTools2.dialogs.glyph import switchGlyphDialog

# run

switchGlyphDialog()
