# [h] close all fonts

'''Close all open fonts.'''

all_fonts = AllFonts()

if len(all_fonts) > 0:
    for font in all_fonts:
        font.close()