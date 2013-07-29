# [h] fit to grid dialog

'''Round different glyph features to a given grid.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import roundToGridDialog

# run

roundToGridDialog()
