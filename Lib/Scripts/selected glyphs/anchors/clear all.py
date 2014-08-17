# [h] clear anchors

"""Delete all anchors in the selected glyphs."""

# imports

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from hTools2.modules.anchors import clear_anchors
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open

# run

f = CurrentFont()

if f is not None:

    glyph_names = get_glyphs(f)
    if len(glyph_names) > 0:
        clear_anchors(f, glyph_names)

    else:
        print no_glyph_selected

else:
    print no_font_open
