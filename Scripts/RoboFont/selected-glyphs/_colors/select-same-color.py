# [h] select glyphs of the same color

'''select all glyphs with the same color as the currently selected glyph'''

from robofab.world import CurrentFont, CurrentGlyph

font = CurrentFont()
glyph = CurrentGlyph()

color = glyph.mark
_same_color_glyphs = []

print 'selecting glyphs with the same color as "%s"...\n' % glyph.name
print '\t',
for glyph in font:
    if glyph.mark == color:
        print glyph.name,
        _same_color_glyphs.append(glyph.name)
font.selection = _same_color_glyphs
font.update()
print 
print '\n...done.\n'
