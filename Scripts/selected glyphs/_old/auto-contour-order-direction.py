# [h] auto countour order & direction

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print 'auto setting contour order & direction...'
for gName in gNames:
    print '\t%s' % gName
    # auto contour order
    f[gName].prepareUndo('auto contour order')
    f[gName].autoContourOrder()
    f[gName].performUndo()    
    # correct direction
    f[gName].prepareUndo('correct path directions')
    f[gName].correctDirection()
    f[gName].performUndo()
print '...done.'
