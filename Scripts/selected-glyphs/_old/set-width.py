# [h] set width for selected glyphs

from hTools2.modules.fileutils import getGlyphs
from hTools2.modules.glyphutils import centerGlyph

# settings

_width = 1000
_center = True

# run script

f = CurrentFont()
gNames = getGlyphs(f)

print 'setting width for selected glyphs...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].prepareUndo('change glyph width')
    f[gName].width = _width
    f[gName].performUndo()
    if _center:
        f[gName].prepareUndo('center glyph')
        centerGlyph(f[gName])
        f[gName].performUndo()
print '...done.\n'
