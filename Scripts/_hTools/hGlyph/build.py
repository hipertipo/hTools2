# [h] build selected glyphs

import hTools2.objects
import hTools2.modules.fontutils

reload(hTools2.objects)
reload(hTools2.modules.fontutils)

from hTools2.objects import hFont
from hTools2.modules.fontutils import get_glyphs

ufo = CurrentFont()
font = hFont(ufo)
glyph_names = get_glyphs(font.ufo)

if len(glyph_names) > 0:
	for glyph_name in glyph_names:
		# print glyph_name,
		try:
			base_glyph, accents = font.project.libs['accents'][glyph_name]
			font.ufo.removeGlyph(glyph_name)
			font.ufo.compileGlyph(glyph_name, base_glyph, accents)
			font.ufo[glyph_name].update()
		except KeyError:
			print 'problem with %s' % glyph_name
	font.ufo.update()
else:
	print 'please select one or more accented glyphs to build.\n'
