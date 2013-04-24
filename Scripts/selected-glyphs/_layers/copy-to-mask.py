# [h] copy to mask

'''Copy selected glyphs in one font to the mask layer of another font.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.dialogs
    reload(hTools2.dialogs)

# import

from hTools2.dialogs import copyToMaskDialog

# run

copyToMaskDialog()
