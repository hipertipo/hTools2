# [h] slide glyphs

'''Slide selected glyphs interactively with a slider.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# imports

from hTools2.dialogs.glyphs import slideGlyphsDialog

# run

slideGlyphsDialog()
