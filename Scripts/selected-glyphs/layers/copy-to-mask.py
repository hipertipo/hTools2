# [h] copy to mask

'''Copy selected glyphs in one font to the mask layer of another font.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs.glyphs
    reload(hTools2.dialogs.glyphs)

# import

from hTools2.dialogs.glyphs import copyToMaskDialog

# run

copyToMaskDialog()
