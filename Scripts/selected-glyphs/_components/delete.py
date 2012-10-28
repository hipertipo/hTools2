# [h] delete components

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

# import

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import get_glyphs

# functions

def decompose_glyph(glyph):
    if len(glyph.components) > 0:
        for component in glyph.components:
            glyph.removeComponent(component)
        glyph.update()

# settings

_foreground = True
_layers = True

# run

f = CurrentFont()
glyph_names = get_glyphs(f)
layer_names = f.layerOrder

if len(glyph_names) > 0:
    print 'deleting components in selected glyphs...',
    for glyph_name in glyph_names:
        if _foreground:
            g = f[glyph_name]
            decompose_glyph(g)
        if _layers:
            for layer_name in layer_names:
                g = f[glyph_name].getLayer(layer_name)
                decompose_glyph(g) 
    print 'done.\n'
else:
    print 'please select a few glyphs first.\n'
