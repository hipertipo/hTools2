# [h] build selected glyphs

from hTools2.objects import hFont
from hTools2.modules.fontutils import get_glyphs

ufo = CurrentFont()
font = hFont(ufo)
glyph_names = get_glyphs(font.ufo)

if len(glyph_names) > 0:
	for glyph_name in glyph_names:
		# accents
		if font.project.libs['accents'].has_key(glyph_name):
			base_glyph, accents = font.project.libs['accents'][glyph_name]
			font.ufo.removeGlyph(glyph_name)
			font.ufo.compileGlyph(glyph_name, base_glyph, accents)
			font.ufo[glyph_name].update()
		# composed
		elif font.project.libs['composed'].has_key(glyph_name):
			font.ufo.newGlyph(glyph_name, clear=True)
			components = font.project.libs['composed'][glyph_name]
			_offset_x, _offset_y = 0, 0
			_scale_x, _scale_y = 1, 1
			for component in components:
				font.ufo[glyph_name].appendComponent(component, (_offset_x, _offset_y), (_scale_x, _scale_y))
				_offset_x += font.ufo[component].width
			font.ufo[glyph_name].update()
		# not composed
		else:
			print '%s is not composed.\n' % glyph_name
	# done
	font.ufo.update()

else:
	print 'please select one or more accented glyphs to build.\n'
