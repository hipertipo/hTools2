# [h] set sidebearings for selected glyphs

from hTools2.modules.fileutils import getGlyphs

# settings

_left = 0
_right = 0

# run script

f = CurrentFont()
gNames = getGlyphs(f)

if _left is None and _right is None:
    print 'action aborted, no value given.\n'

else:
    print 'setting sidebearings for selected glyphs...'
    print '\tleft: %s, right: %s' % (_left, _right)
    for gName in gNames:
        print '\t%s' % gName
        if _left is not None:
            f[gName].prepareUndo('change left sidebearing')
            f[gName].leftMargin = _left
            f[gName].performUndo()
        if _right is not None:
            f[gName].prepareUndo('change right sidebearing')
            f[gName].rightMargin = _right
            f[gName].performUndo()
    print '...done.\n'

