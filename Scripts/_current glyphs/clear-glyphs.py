# [h] clear glyphs

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print 'emptying selected glyphs...'
for gName in gNames:
    print '\t%s' % gName
    f.newGlyph(gName, clear=True)
print '...done.'
