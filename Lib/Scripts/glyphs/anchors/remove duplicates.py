# [h] remove duplicate anchors

from hTools2.modules.anchors import clear_duplicate_anchors
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

f = CurrentFont()

if f is not None:

    glyph_names = get_glyphs(f)

    if len(glyph_names) > 0:

        print 'cleaning duplicate anchors...\n'

        for glyph_name in glyph_names:
            g = f[glyph_name]
            print '\t%s: %s ->' % (glyph_name, len(g.anchors)),
            clear_duplicate_anchors(g)
            print len(g.anchors)

        print
        print '...done.\n'

    else:
        print no_glyph_selected

else:
    print no_font_open
