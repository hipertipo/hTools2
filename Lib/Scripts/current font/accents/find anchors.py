# [h] mark glyphs with anchors

# imports

from hTools2.modules.color import random_color
from hTools2.modules.fontutils import clear_colors
from hTools2.modules.messages import no_font_open

# options

clear = False

# run!

f = CurrentFont()

if f is not None:
    if clear:
        clear_colors(f)
    color = random_color()
    for g in f:
        if len(g.anchors) > 0:
            g.mark = color

else:
    print no_font_open
