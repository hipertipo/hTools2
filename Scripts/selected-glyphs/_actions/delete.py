# [h] remove selected glyphs

'delete selected glyphs in font'

from hTools2.modules.fontutils import get_glyphs

f = CurrentFont()
gNames = get_glyphs(f)
for gName in gNames:
	f.removeGlyph(gName)
f.update()
