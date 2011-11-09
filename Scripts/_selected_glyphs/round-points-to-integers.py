# [h] round point coordenates to integers

from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()
gNames = getGlyphs(f)

print 'rounding point positions...'
for gName in gNames:
    print '\trounding %s' % gName
    f[gName].prepareUndo('round point positions')
    f[gName].round()
    f[gName].performUndo()
print '...done.\n'
