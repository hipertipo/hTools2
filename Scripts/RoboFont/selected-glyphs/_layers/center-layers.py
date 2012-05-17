# [h] center layers

from hTools2.modules.glyphutils import *

_guides = True 

f = CurrentFont()

if f is not None:
    layers = f.layerOrder
    # current glyph
    g = CurrentGlyph()
    if g is not None:
        center_glyph_layers(g, layers)
    else:
        glyph_names = f.selection    
        # selected glyphs
        if len(glyph_names) > 0:
            for glyph_name in glyph_names:
                center_glyph_layers(f[glyph_name], layers)            
        else:
            print 'please select one or more glyphs first.\n'        
            
else:
    print 'please open a font first.\n'
