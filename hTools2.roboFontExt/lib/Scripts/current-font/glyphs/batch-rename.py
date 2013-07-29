# [h] batch rename glyphs

'''Batch rename glyphs in font based on a list.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import batchRenameGlyphs

# run

batchRenameGlyphs()
