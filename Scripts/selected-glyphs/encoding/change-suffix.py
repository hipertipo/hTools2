# [h] change glyph suffix

'''Change the existing suffix of selected glyphs by a new one.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import changeSuffixDialog

# run

changeSuffixDialog()
