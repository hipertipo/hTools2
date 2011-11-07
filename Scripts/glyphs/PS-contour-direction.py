# [h] set PS countour direction

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print 'auto contour order/direction...'
for gName in gNames:
    print '\trounding %s' % gName
    f[gName].autoContourOrder()
    f[gName].correctDirection()
    f[gName].leftMargin = 0
    f[gName].rightMargin = 0    
print '...done.'