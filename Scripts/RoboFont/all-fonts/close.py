# [h] : close all open fonts

_all_fonts = AllFonts()

if len(_all_fonts) > 0:
	for font in _all_fonts:
		font.close()
 