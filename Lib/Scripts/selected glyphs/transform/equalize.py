import hTools2.extras.equalize
reload(hTools2.extras.equalize)

from hTools2.extras.equalize import equalize_curves
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

f = CurrentFont()

if f is not None:
    glyphs = get_glyphs(f)

    if len(glyphs) > 0:
        print 'equalizing curves...'
        print '\t',
        for glyph in sorted(glyphs):
            print glyph,
            equalize_curves(f[glyph])
        print
        print '...done.'

    else:
         print no_glyph_selected

else:
    print no_font_open

