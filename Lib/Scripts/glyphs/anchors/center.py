# [h] center anchors

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open

anchor_names = ['top', 'bottom']

f = CurrentFont()

if f is not None:
    glyph_names = get_glyphs(f)
    for glyph_name in glyph_names:
        glyph = f[glyph_name]
        anchors = glyph.anchors
        if len(anchors) > 0:
            glyph.prepareUndo('center anchors')
            for anchor in anchors:
                if anchor.name in anchor_names:
                    anchor.x = glyph.bounds[2] * 0.5
            glyph.changed()
            glyph.performUndo()
else:
    print no_font_open
