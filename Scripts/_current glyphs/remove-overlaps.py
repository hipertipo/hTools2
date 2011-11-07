# [h] remove overlaps

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print 'removing overlaps...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].removeOverlap()
print '...done.\n'
