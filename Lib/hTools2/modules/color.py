# [h] hTools2.modules.color

"""Simple tools for working with colors."""

# import

import random
from hTools2.modules.sysutils import _ctx
from hTools2.extras.colorsys import *

#-----------
# functions
#-----------

def random_color(alpha=1.0):
    """Return a random color."""
    # FontLab
    if _ctx == 'FontLab':
        c = int(255 * random.random())
    # RoboFont & NoneLab
    else:
        R, G, B = hsv_to_rgb(random.random(), 1.0, 1.0)
        c = (R, G, B, alpha)
    return c

def clear_colors(font):
    """Clear the color from all glyph cells in the font."""
    for glyph_name in font.keys():
        clear_color(font[glyph_name])
    font.update()

def clear_color(glyph):
    """Clear the color of a glyph cell."""
    # FontLab
    if _ctx == 'FontLab':
        g.mark = 0
    # RoboFont & NoneLab
    else:
        glyph.mark = None # (1, 1, 1, 0)
    glyph.update()

def convert_to_1(R, G, B, A=None):
    r = R / 255.0
    g = G / 255.0
    b = B / 255.0
    if A:
        a = A / 255.0
        return (r, g, b, a)
    else:
        return (r, g, b)

def convert_to_255(r, g, b, a=None):
    R = r * 255.0
    G = g * 255.0
    B = b * 255.0
    if a:
        A = a * 255.0
        return (R, G, B, A)
    else:
        return (R, G, B)

def convert_to_nscolor(r, g, b, a=1.0):
    from AppKit import NSColor
    nscolor = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)
    return nscolor

def cubic(t, a, b):
    weight = t * t * (3 - 2*t)
    return a + weight * (b - a)

#------------------------
# color mode conversions
#------------------------

def hex_to_rgb(value):
    """Convert hex color to RGB (range 1.0)."""
    value = value.lstrip('#')
    lv = len(value)
    rgb = tuple()
    for i in range(0, lv, lv/3):
        rgb += ( int(value[i:i+lv/3], 16) / 255., )
    return rgb

def rgb_to_hex(rgb):
    """Convert RGB color (range 1.0) to hex."""
    return '%02x%02x%02x' % rgb

def ryb_to_rgb(r, y, b):
    """Convert RYB color to RGB (range 1.0)."""
    # http://stackoverflow.com/a/14116553
    # red
    x0, x1 = cubic(b, 1.0, 0.163), cubic(b, 1.0, 0.0)
    x2, x3 = cubic(b, 1.0, 0.5), cubic(b, 1.0, 0.2)
    y0, y1 = cubic(y, x0, x1), cubic(y, x2, x3)
    red = cubic(r, y0, y1)
    # green
    x0, x1 = cubic(b, 1.0, 0.373), cubic(b, 1.0, 0.66)
    x2, x3 = cubic(b, 0., 0.), cubic(b, 0.5, 0.094)
    y0, y1 = cubic(y, x0, x1), cubic(y, x2, x3)
    green = cubic(r, y0, y1)
    # blue
    x0, x1 = cubic(b, 1.0, 0.6), cubic(b, 0.0, 0.2)
    x2, x3 = cubic(b, 0.0, 0.5), cubic(b, 0.0, 0.0)
    y0, y1 = cubic(y, x0, x1), cubic(y, x2, x3)
    blue = cubic(r, y0, y1)
    # done
    return (red, green, blue)

def RGB_to_nodebox_color((R, G, B), ctx, alpha=1.0):
    """Convert RGB color to a NodeBox ``Color`` object."""
    colors = ctx.ximport("colors")
    _alpha = 255 * alpha
    _color = colors.rgb(R, G, B, _alpha, range=255)
    return _color

#--------------
# named colors
#--------------

# A dictionary with color names and RGBa values.
named_colors = {
    'red' : hsv_to_rgb(.0, 1, 1) + (1,),
    'orange' : hsv_to_rgb(.11, 1, 1) + (1,),
    'yellow' : hsv_to_rgb(.15, 1, 1) + (1,),
    'green' : hsv_to_rgb(.35, 1, 1) + (1,),
    'cyan' : hsv_to_rgb(.5, 1, 1) + (1,),
    'blue' : hsv_to_rgb(.7, 1, 1) + (1,),
    'purple' : hsv_to_rgb(.8, 1, 1) + (1,),
    'pink' : hsv_to_rgb(.9, 1, 1) + (1,),
}

#------------------
# solarized colors
#------------------

def solarized_color(name):
    """Return an ``RGB`` color for a solarized color name."""
    # name is color group
    if name in solarized_groups.keys():
        _colors = []
        for _color in solarized_groups[name]:
            _colors.append(solarized_colors[_color])
        return _colors
    # name is color
    elif name in solarized_colors.keys():
        return solarized_colors[name]
    # name has no meaning
    else:
        print 'name %s is not a solarized group or color.\n' % name

# Solarized colors by name and RGB values.
solarized_colors = {
    # dark
    'base03' : (0, 43, 54),
    'base02' : (7, 54, 66),
    # bright
    'base2' : (238, 232, 213),
    'base3' : (253, 246, 227),
    # content
    'base01' : (88, 110, 117),
    'base00' : (101, 123, 131),
    'base0' : (131, 148, 150),
    'base1' : (147, 161, 161),
    # accent
    'yellow' : (181, 137, 0),
    'orange' : (203, 75, 22),
    'red' : (220, 50, 47),
    'magenta' : (211, 54, 130),
    'violet' : (108, 113, 196),
    'blue' : (38, 139, 210),
    'cyan' : (42, 161, 152),
    'green' : (133, 152, 0),
}

# Solarized colors by name, divided in groups.
solarized_groups = {
    'colors' : [ 'yellow', 'orange', 'red', 'magenta', 'violet', 'blue', 'cyan', 'green' ],
    'dark' : [ 'base03', 'base02' ],
    'bright' : [ 'base3', 'base2' ],
    'content' : [ 'base01', 'base00', 'base0', 'base1' ],
}

#-----------------
# X11 color names
#-----------------

def x11_color(name):
    """Return an ``RGB`` color for an x11 color name."""
    # name is color
    _color_names = x11_colors.keys()
    if name in _color_names:
        return x11_colors[name]
    else:
        # build lowercase dict
        _color_names_lower = {}
        for color_name in _color_names:
            _color_names_lower[color_name.lower()] = color_name
        # try name in lowercase
        if name in _color_names_lower.keys():
            color_name = _color_names_lower[name]
            return x11_colors[color_name]
        # name is not x11 color
        else:
            print 'name %s is not a x11 group or color.\n' % name

# X11 colors by name and `(R,G,B)` values.
x11_colors = {
    # red colors
    'IndianRed' : (205, 92, 92),
    'LightCoral' : (240, 128, 128),
    'Salmon' : (250, 128, 114),
    'DarkSalmon' : (233, 150, 122),
    'LightSalmon' : (255, 160, 122),
    'Red' : (255, 0, 0),
    'Crimson' : (220, 20, 60),
    'FireBrick' : (178, 34, 34),
    'DarkRed' : (139, 0, 0),
    # pink colors
    'Pink' : (255, 192, 203),
    'LightPink' : (255, 182, 193),
    'HotPink' : (255, 105, 180),
    'DeepPink' : (255, 20, 147),
    'MediumVioletRed' : (199, 21, 133),
    'PaleVioletRed' : (219, 112, 147),
    # orange colors
    'LightSalmon' : (255, 160, 122),
    'Coral' : (255, 127, 80),
    'Tomato' : (255, 99, 71),
    'OrangeRed' : (255, 69, 0),
    'DarkOrange' : (255, 140, 0),
    'Orange' : (255, 165, 0),
    # yellow colors
    'Gold' : (255, 215, 0),
    'Yellow' : (255, 255, 0),
    'LightYellow' : (255, 255, 224),
    'LemonChiffon' : (255, 250, 205),
    'LightGoldenrodYellow' : (250, 250, 210),
    'PapayaWhip' : (255, 239, 213),
    'Moccasin' : (255, 228, 181),
    'PeachPuff' : (255, 218, 185),
    'PaleGoldenrod' : (238, 232, 170),
    'Khaki' : (240, 230, 140),
    'DarkKhaki' : (189, 183, 107),
    # purple colors
    'Lavender' : (230, 230, 250),
    'Thistle' : (216, 191, 216),
    'Plum' : (221, 160, 221),
    'Violet' : (238, 130, 238),
    'Orchid' : (218, 112, 214),
    'Fuchsia' : (255, 0, 255),
    'Magenta' : (255, 0, 255),
    'MediumOrchid' : (186, 85, 211),
    'MediumPurple' : (147, 112, 219),
    'BlueViolet' : (138, 43, 226),
    'DarkViolet' : (148, 0, 211),
    'DarkOrchid' : (153, 50, 204),
    'DarkMagenta' : (139, 0, 139),
    'Purple' : (128, 0, 128),
    'Indigo' : (75, 0, 130),
    'DarkSlateBlue' : (72, 61, 139),
    'SlateBlue' : (106, 90, 205),
    'MediumSlateBlue' : (123, 104, 238),
    # green colors
    'GreenYellow' : (173, 255, 47),
    'Chartreuse' : (127, 255, 0),
    'LawnGreen' : (124, 252, 0),
    'Lime' : (0, 255, 0),
    'LimeGreen' : (50, 205, 50),
    'PaleGreen' : (152, 251, 152),
    'LightGreen' : (144, 238, 144),
    'MediumSpringGreen' : (0, 250, 154),
    'SpringGreen' : (0, 255, 127),
    'MediumSeaGreen' : (60, 179, 113),
    'SeaGreen' : (46, 139, 87),
    'ForestGreen' : (34, 139, 34),
    'Green' : (0, 128, 0),
    'DarkGreen' : (0, 100, 0),
    'YellowGreen' : (154, 205, 50),
    'OliveDrab' : (107, 142, 35),
    'Olive' : (128, 128, 0),
    'DarkOliveGreen' : (85, 107, 47),
    'MediumAquamarine' : (102, 205, 170),
    'DarkSeaGreen' : (143, 188, 143),
    'LightSeaGreen' : (32, 178, 170),
    'DarkCyan' : (0, 139, 139),
    'Teal' : (0, 128, 128),
    # blue/cyan colors
    'Aqua' : (0, 255, 255),
    'Cyan' : (0, 255, 255),
    'LightCyan' : (224, 255, 255),
    'PaleTurquoise' : (175, 238, 238),
    'Aquamarine' : (127, 255, 212),
    'Turquoise' : (64, 224, 208),
    'MediumTurquoise' : (72, 209, 204),
    'DarkTurquoise' : (0, 206, 209),
    'CadetBlue' : (95, 158, 160),
    'SteelBlue' : (70, 130, 180),
    'LightSteelBlue' : (176, 196, 222),
    'PowderBlue' : (176, 224, 230),
    'LightBlue' : (173, 216, 230),
    'SkyBlue' : (135, 206, 235),
    'LightSkyBlue' : (135, 206, 250),
    'DeepSkyBlue' : (0, 191, 255),
    'DodgerBlue' : (30, 144, 255),
    'CornflowerBlue' : (100, 149, 237),
    'RoyalBlue' : (65, 105, 225),
    'Blue' : (0, 0, 255),
    'MediumBlue' : (0, 0, 205),
    'DarkBlue' : (0, 0, 139),
    'Navy' : (0, 0, 128),
    'MidnightBlue' : (25, 25, 112),
    # brown colors
    'Cornsilk' : (255, 248, 220),
    'BlanchedAlmond' : (255, 235, 205),
    'Bisque' : (255, 228, 196),
    'NavajoWhite' : (255, 222, 173),
    'Wheat' : (245, 222, 179),
    'BurlyWood' : (222, 184, 135),
    'Tan' : (210, 180, 140),
    'RosyBrown' : (188, 143, 143),
    'SandyBrown' : (244, 164, 96),
    'Goldenrod' : (218, 165,  32),
    'DarkGoldenrod' : (184, 134, 11),
    'Peru' : (205, 133, 63),
    'Chocolate' : (210, 105, 30),
    'SaddleBrown' : (139, 69, 19),
    'Sienna' : (160, 82, 45),
    'Brown' : (165, 42, 42),
    'Maroon' : (128, 0, 0),
    # white colors
    'White' : (255, 255, 255),
    'Snow' : (255, 250, 250),
    'Honeydew' : (240, 255, 240),
    'MintCream' : (245, 255, 250),
    'Azure' : (240, 255, 255),
    'AliceBlue' : (240, 248, 255),
    'GhostWhite' : (248, 248, 255),
    'WhiteSmoke' : (245, 245, 245),
    'Seashell' : (255, 245, 238),
    'Beige' : (245, 245, 220),
    'OldLace' : (253, 245, 230),
    'FloralWhite' : (255, 250, 240),
    'Ivory' : (255, 255, 240),
    'AntiqueWhite' : (250, 235, 215),
    'Linen' : (250, 240, 230),
    'LavenderBlush' : (255, 240, 245),
    'MistyRose' : (255, 228, 225),
    # gray colors
    'Gainsboro' : (220, 220, 220),
    'LightGrey' : (211, 211, 211),
    'Silver' : (192, 192, 192),
    'DarkGray' : (169, 169, 169),
    'Gray' : (128, 128, 128),
    'DimGray' : (105, 105, 105),
    'LightSlateGray' : (119, 136, 153),
    'SlateGray' : (112, 128, 144),
    'DarkSlateGray' : (47, 79, 79),
    'Black' : (0, 0, 0),
}

# X11 colors by name, divided in groups.
x11_groups = {
    'red' : [ 'IndianRed', 'LightCoral', 'Salmon', 'DarkSalmon', 'LightSalmon', 'Red', 'Crimson', 'FireBrick', 'DarkRed' ],
    'pink' : [ 'Pink', 'LightPink', 'HotPink', 'DeepPink', 'MediumVioletRed', 'PaleVioletRed' ],
    'orange' : [ 'LightSalmon', 'Coral', 'Tomato', 'OrangeRed', 'DarkOrange', 'Orange' ],
    'yellow' : [ 'Gold', 'Yellow', 'LightYellow', 'LemonChiffon', 'LightGoldenrodYellow', 'PapayaWhip', 'Moccasin', 'PeachPuff', 'PaleGoldenrod', 'Khaki', 'DarkKhaki' ],
    'purple' : [ 'Lavender', 'Thistle', 'Plum', 'Violet', 'Orchid', 'Fuchsia', 'Magenta', 'MediumOrchid', 'MediumPurple', 'BlueViolet', 'DarkViolet', 'DarkOrchid', 'DarkMagenta', 'Purple', 'Indigo', 'DarkSlateBlue', 'SlateBlue', 'MediumSlateBlue' ],
    'green' : [ 'GreenYellow', 'Chartreuse', 'LawnGreen', 'Lime', 'LimeGreen', 'PaleGreen', 'LightGreen', 'MediumSpringGreen', 'SpringGreen', 'MediumSeaGreen', 'SeaGreen', 'ForestGreen', 'Green', 'DarkGreen', 'YellowGreen', 'OliveDrab', 'Olive', 'DarkOliveGreen', 'MediumAquamarine', 'DarkSeaGreen', 'LightSeaGreen', 'DarkCyan', 'Teal' ],
    'blue' : [ 'Aqua', 'Cyan', 'LightCyan', 'PaleTurquoise', 'Aquamarine', 'Turquoise', 'MediumTurquoise', 'DarkTurquoise', 'CadetBlue', 'SteelBlue', 'LightSteelBlue', 'PowderBlue', 'LightBlue', 'SkyBlue', 'LightSkyBlue', 'DeepSkyBlue', 'DodgerBlue', 'CornflowerBlue', 'RoyalBlue', 'Blue', 'MediumBlue', 'DarkBlue', 'Navy', 'MidnightBlue' ],
    'brown' : [ 'Cornsilk', 'BlanchedAlmond', 'Bisque', 'NavajoWhite', 'Wheat', 'BurlyWood', 'Tan', 'RosyBrown', 'SandyBrown', 'Goldenrod', 'DarkGoldenrod', 'Peru', 'Chocolate', 'SaddleBrown', 'Sienna', 'Brown', 'Maroon' ],
    'white' : [ 'White', 'Snow', 'Honeydew', 'MintCream', 'Azure', 'AliceBlue', 'GhostWhite', 'WhiteSmoke', 'Seashell', 'Beige', 'OldLace', 'FloralWhite', 'Ivory', 'AntiqueWhite', 'Linen', 'LavenderBlush', 'MistyRose' ],
    'gray' : [ 'Gainsboro', 'LightGrey', 'Silver', 'DarkGray', 'Gray', 'DimGray', 'LightSlateGray', 'SlateGray', 'DarkSlateGray', 'Black', ]
}
