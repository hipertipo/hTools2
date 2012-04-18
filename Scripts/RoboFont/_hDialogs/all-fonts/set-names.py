# [h] set font names for all open fonts

from hTools2.modules.fontinfo import set_names_from_path

all_fonts = AllFonts()

if len(all_fonts) > 0:
	for font in all_fonts:
		set_names_from_path(font)
		font.update()