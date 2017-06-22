# [h] close all fonts

try:
    from mojo.roboFont import AllFonts
except ImportError:
    from robofab.world import AllFonts

from hTools2.modules.messages import no_font_open

all_fonts = AllFonts()

if len(all_fonts) > 0:
    for font in all_fonts:
        font.close()

else:
    no_font_open
