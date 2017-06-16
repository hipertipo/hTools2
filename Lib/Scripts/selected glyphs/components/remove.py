# [h] remove components

'''Remove components in selected glyphs.'''

import hTools2.modules.glyphutils
reload(hTools2.modules.glyphutils)

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import remove_components
from hTools2.modules.messages import no_font_open, no_glyph_selected

# settings

foreground = True
layers     = True

# run

f = CurrentFont()
if f is not None:
    glyph_names = get_glyphs(f)
    layer_names = f.layerOrder
    if len(glyph_names) > 0:
        print 'removing components in selected glyphs...',
        for glyph_name in glyph_names:
            if foreground:
                g = f[glyph_name]
                # g.prepareUndo('remove components') # doesn’t work?
                remove_components(g)
                # g.performUndo()
            if layers:
                for layer_name in layer_names:
                    g = f[glyph_name].getLayer(layer_name)
                    # g.prepareUndo('remove components')
                    remove_components(g)
                    # g.performUndo()
        print 'done.\n'
    # no glyph selected
    else:
        print no_glyph_selected
# no font open
else:
    print no_font_open
