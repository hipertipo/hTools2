# [h] center layers

#-----------
# functions
#-----------

def draw_bounds(g, (x1, y1, x2, y2), (x3, y3)):
    # x guides
    g.addGuide((x1, 0), 90, name="x_min")
    g.addGuide((x2, 0), 90, name="x_max")
    g.addGuide((x3, 0), 90, name="x_mid")
    # y guides
    g.addGuide((0, y1), 0, name="y_min")
    g.addGuide((0, y2), 0, name="y_max")
    g.addGuide((0, y3), 0, name="y_mid")
    # done
    g.update()

def clear_guides(glyph):
    for guide in glyph.guides:
        glyph.removeGuide(guide)

def get_bounds(g, layer_names):
    lowest_x = False
    lowest_y = False
    highest_x = False
    highest_y = False
    for layer_name in layer_names:
        glyph = g.getLayer(layer_name)
        if glyph.box is not None:
            xMin, yMin, xMax, yMax = glyph.box
            # lowest x
            if not lowest_x:
                lowest_x = xMin
            else:
                if xMin < lowest_x:
                   lowest_x = xMin
            # lowest y            
            if not lowest_y:
                lowest_y = yMin
            else:
                if yMin < lowest_y:
                   lowest_y = yMin
            # highest x
            if not highest_x:
                highest_x = xMax
            else:
                if xMax > highest_x:
                    highest_x = xMax
            # highest y
            if not highest_y:
                highest_y = yMax
            else:
                if yMax > highest_y:
                    highest_y = yMax
    # done
    return (lowest_x, lowest_y, highest_x, highest_y)

def get_middle((lo_x, lo_y, hi_x, hi_y)):
    width_all = hi_x - lo_x
    height_all = hi_y - lo_y
    middle_x = lo_x + (width_all * .5)
    middle_y = lo_x + (height_all * .5)
    return (middle_x, middle_y)

def center_layers(g, layer_names, (middle_x, middle_y)):
    for layer_name in layer_names:
        glyph = g.getLayer(layer_name)
        if glyph.box is not None:
            xMin, yMin, xMax, yMax = glyph.box
            w = xMax - xMin
            h = yMax - yMin
            center_x = xMin + (w * .5)
            center_y = yMin + (h * .5)
            shift_x = middle_x - center_x
            shift_y = middle_y - center_y
            glyph.move((shift_x, shift_y))
        g.update()

def center_glyph_layers(g, layers, guides=True):
    # get center
    _bounds = get_bounds(g, layers)
    _middle = get_middle(_bounds)
    # draw bounds
    if guides:
        clear_guides(g)
        draw_bounds(g, _bounds, _middle)
    # center layers
    center_layers(g, layers, _middle)

#------------
# the script
#------------

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

