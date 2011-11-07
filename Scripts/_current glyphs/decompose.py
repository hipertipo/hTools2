# [h] decompose selected glyphs

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print 'decomposing selected glyphs...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].prepareUndo()
    f[gName].decompose()
print '...done.'
