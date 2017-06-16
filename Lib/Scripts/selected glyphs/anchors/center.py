# [h] center anchors

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

anchor_names = ['top', 'bottom']

f = CurrentFont()

if f is not None:

    glyph_names = get_glyphs(f)

    if len(glyph_names) > 0:
        for glyph_name in glyph_names:
            glyph = f[glyph_name]
            anchors = glyph.anchors
            if len(anchors) > 0:
                for anchor in anchors:
                    if anchor.name in anchor_names:
                        anchor.x = glyph.box[2] * 0.5
                glyph.update()

    else:
        print no_glyph_selected

else:
    print no_font_open
