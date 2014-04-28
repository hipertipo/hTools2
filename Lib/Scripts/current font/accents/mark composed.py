# [h] mark composed glyphs

# imports

from hTools2.modules.fontutils import clear_colors, mark_composed_glyphs
from hTools2.modules.messages import no_font_open

# parameters

clear = False

# run!

f = CurrentFont()

if f is not None:
    if clear:
        clear_colors(f)
    mark_composed_glyphs(f)

else:
    print no_font_open
