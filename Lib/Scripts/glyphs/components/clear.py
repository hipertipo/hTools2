# [h] remove components

'''Remove components in selected glyphs.'''

from mojo.roboFont import CurrentFont
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import remove_components
from hTools2.modules.messages import no_font_open, no_glyph_selected

def delete_components(glyph):
    if len(glyph.components) > 0:
        glyph.prepareUndo('delete components')
        for component in glyph.components:
            glyph.removeComponent(component)
        glyph.changed()
        glyph.performUndo()

foreground = True
layers = False

f = CurrentFont()

if f is not None:

    glyph_names = get_glyphs(f)
    layer_names = f.layerOrder

    if len(glyph_names) > 0:
        print 'removing components in selected glyphs...',
        for glyph_name in glyph_names:
            if foreground:
                g = f[glyph_name]
                delete_components(g)
            if layers:
                for layer_name in layer_names:
                    g = f[glyph_name].getLayer(layer_name)
                    delete_components(g)
        print 'done.\n'

    # no glyph selected
    else:
        print no_glyph_selected

# no font open
else:
    print no_font_open
