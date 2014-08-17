# [h] clear unicodes

"""Clear unicode values from selected glyphs."""

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open

f = CurrentFont()

if f is None:
    glyph_names = get_glyphs(f)
    if len(glyph_names) > 0:
        for glyph_name in glyph_names:
            f[glyph_name].unicodes = []
    # no glyph selected
    else:
        print no_glyph_selected
# no font open
else:
    print no_font_open
