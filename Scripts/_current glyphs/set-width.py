# [h] set width for selected glyphs

from hTools2.modules.fileutils import getGlyphs

def centerGlyph(glyph):
    whitespace = glyph.leftMargin + glyph.rightMargin
    glyph.leftMargin = whitespace / 2
    glyph.rightMargin = whitespace / 2    

f = CurrentFont()
gNames = getGlyphs(f)

# settings

_width = 1000
_center = True

print 'setting width for selected glyphs...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].prepareUndo()
    f[gName].width = _width
    if _center:
        centerGlyph(f[gName])
print '...done.\n'

