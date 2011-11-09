# [h] remove overlaps

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print 'removing overlaps...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].prepareUndo('remove overlaps')
    f[gName].removeOverlap()
    f[gName].performUndo()
print '...done.\n'
