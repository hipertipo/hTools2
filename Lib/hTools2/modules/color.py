# [h] hTools2.modules.color

'''
hTools2.modules.color
=====================

Functions
---------

### `random_color()`

Returns a random color.

If the context is `RoboFont` or `NoneLab`, the returned value is a tuple of `(R,G,B,alpha)` values; if the context is FontLab, the returned value is an integer between `0` and `255`.

Independent of the context, the visual result is a always color with random variation in the `hue` dimension, and constant saturation, brightness and opacity values.

    # RoboFont / NoneLab
    from hTools2.modules.color import random_color
    c = random_color()
    print c

    >>> (0.0, 0.2447768481540229, 1.0, 1.0)

    # FontLab
    from hTools2.modules.color import random_color
    c = random_color()
    print c

    >>> (196.0)

### `clear_colors(font)`

Removes the color of all glyphs in the given `font`.

    from hTools2.modules.color import clear_colors
    font = CurrentFont()
    clear_colors(font)

### `clear_color(glyph)`

Removes the color of the given `glyph`.

    from hTools2.modules.color import clear_color
    font = CurrentFont()
    clear_color(font['a'])

### `RGB_to_nodebox_color((R, G, B), ctx)`

Takes a tuple of `(R,G,B)` values and returns a NodeBox `color` object.

The example below shows some sample code in NodeBox. The `_ctx` object is native to Nodebox, and gives access to its canvas, drawing state, primitives etc.

    from hTools2.modules.color import RGB_to_nodebox_color
    print RGB_to_nodebox_color((0, 1, 0), _ctx)

    >>> Color(0.000, 0.004, 0.000, 1.000)

### `paint_groups(font)`

Paints the glyphs in the `font` according to their groups. If a `groups_order` lib is available, it is used to set the order of the glyphs in the font.

    from hTools2.modules.color import paint_groups
    font = CurrentFont()
    paint_groups(font)

Objects
-------

### `named_colors`

A dictionary with color names and their corresponding color values, as `(R,G,B,alpha)` tuples.

    from hTools2.modules.color import named_colors
    print named_colors.keys()

    >>> ['blue', 'purple', 'pink', 'green', 'yellow', 'orange', 'cyan', 'red']

    print named_colors['orange']

    >>> (1, 0.66, 0.0, 1)

'''

from random import random

from hTools2.modules.fontutils import *
from hTools2.modules.sysutils import _ctx
from hTools2.extras.colorsys import *

def random_color():
    # FontLab
    if _ctx == 'FontLab':
        c = int(255 * random())
    # RoboFont & NoneLab
    else:
        R, G, B = hsv_to_rgb(random(), 1.0, 1.0)
        _alpha = 1.0
        c = (R, G, B, _alpha)
    return c

def clear_colors(font):
    for gName in font.keys():
        clear_color(font[gName])
    font.update()

def clear_color(glyph):
    # FontLab
    if _ctx == 'FontLab':
        g.mark = 0
    # RoboFont & NoneLab
    else:   
        glyph.mark = (1, 1, 1, 0)
    glyph.update()

def RGB_to_nodebox_color((R, G, B), ctx, alpha=1.0):
    colors = ctx.ximport("colors")
    _alpha = 255 * alpha
    _color = colors.rgb(R, G, B, _alpha, range=255)
    return _color

def paint_groups(f, crop=False):
    if len(f.groups) > 0:
        clear_colors(f)
        count = 0
        _order = []
        if f.lib.has_key('groups_order'):
            groups = f.lib['groups_order']
        else:
            groups = f.groups.keys()
        for group in groups:
            color_step = 1.0 / len(f.groups)
            color = color_step * count
            R, G, B = hls_to_rgb(color, 0.5, 1.0)
            for glyph_name in f.groups[group]:
                if f.has_key(glyph_name) is not True:
                    f.newGlyph(glyph_name)
                _order.append(glyph_name)
                f[glyph_name].mark = (R, G, B, .5)
                f[glyph_name].update()
            count += 1
        f.glyphOrder = _order
        f.update()
    if crop:
        crop_glyphset(f, _order)
    else:
        print 'font has no groups.\n'

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

#-----------
# solarized
#-----------

def solarized(name):
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

solarized_groups = {
    'colors' : [ 'yellow', 'orange', 'red', 'magenta', 'violet', 'blue', 'cyan', 'green' ],
    'dark' : [ 'base03', 'base02' ],
    'bright' : [ 'base3', 'base2' ],
    'content' : [ 'base01', 'base00', 'base0', 'base1' ],
}

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
