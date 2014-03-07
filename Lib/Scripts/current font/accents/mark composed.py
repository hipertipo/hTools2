# [h] mark composed glyphs

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import clear_colors, mark_composed_glyphs
from hTools2.modules.messages import no_font_open

f = CurrentFont()

if f is not None:
    clear_colors(f)
    mark_composed_glyphs(f)

else:
    print no_font_open
