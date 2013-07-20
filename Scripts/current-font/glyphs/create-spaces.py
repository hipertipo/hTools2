# [h] create space glyphs

'''Create special space glyphs in font. (en-space, thin space etc)'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import createSpaceGlyphsDialog

# run

createSpaceGlyphsDialog()
