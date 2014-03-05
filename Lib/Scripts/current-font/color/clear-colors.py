# [h] clear colors

from mojo.roboFont import CurrentFont

from hTools2.modules.color import clear_colors
from hTools2.modules.messages import no_font_open

f = CurrentFont()

if f is not None:
    clear_colors(f)

else:
    print no_font_open
