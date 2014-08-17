# [h] remove components

"""Remove components in selected glyphs."""

# import

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_font_open, no_glyph_selected

# functions

def decompose_glyph(glyph):
    if len(glyph.components) > 0:
        for component in glyph.components:
            glyph.removeComponent(component)
        glyph.update()

# settings

foreground = True
layers = True

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
                decompose_glyph(g)
            if layers:
                for layer_name in layer_names:
                    g = f[glyph_name].getLayer(layer_name)
                    decompose_glyph(g)
        print 'done.\n'
    # no glyph selected
    else:
        print no_glyph_selected
# no font open
else:
    print no_font_open
