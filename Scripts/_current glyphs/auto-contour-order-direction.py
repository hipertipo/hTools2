# [h] auto countour order & direction

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print 'auto setting contour order & direction...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].prepareUndo()
    f[gName].autoContourOrder()
    f[gName].correctDirection()
    f[gName].leftMargin = 0
    f[gName].rightMargin = 0
print '...done.'
