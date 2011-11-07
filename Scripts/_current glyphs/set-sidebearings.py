# [h] set sidebearings for selected glyphs

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

# settings

_left = 0
_right = None

if _left is None and _right is None:
    print 'action aborted, no value given.\n'

else:
    print 'setting sidebearings for selected glyphs...'
    print '\tleft: %s, right: %s' % (_left, _right)
    for gName in gNames:
        print '\t%s' % gName
        f[gName].prepareUndo()
        if _left is not None:
            f[gName].leftMargin = _left
        if _right is not None:
            f[gName].rightMargin = _right
    print '...done.\n'
