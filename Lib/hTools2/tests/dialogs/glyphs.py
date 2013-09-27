# [h] open all 'selected glyphs' dialogs

import hTools2.dialogs.glyphs

for dialog in hTools2.dialogs.glyphs.__all__:
    try:
        exec 'D = hTools2.dialogs.glyphs.%s()' % dialog
    except:
        print 'could not open %s' % dialog
