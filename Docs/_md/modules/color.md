### random_color()

Return a random color.

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

### clear_colors(font)

Remove the color of all glyphs in the given `font`.

    from hTools2.modules.color import clear_colors
    font = CurrentFont()
    clear_colors(font)

### clear_color(glyph)

Remove the color of the given `glyph`.

    from hTools2.modules.color import clear_color
    font = CurrentFont()
    clear_color(font['a'])

### RGB_to_nodebox_color((R, G, B), ctx)

Take a tuple of `(R,G,B)` values and return a NodeBox `color` object.

The example below shows some sample code in NodeBox. The `_ctx` object is native to Nodebox, and gives access to its canvas, drawing state, primitives etc.

    from hTools2.modules.color import RGB_to_nodebox_color
    print RGB_to_nodebox_color((0, 1, 0), _ctx)

    >>> Color(0.000, 0.004, 0.000, 1.000)

### paint_groups(font)

Paint the glyphs in the `font` according to their groups. If a `groups_order` lib is available, it is used to set the order of the glyphs in the font.

    from hTools2.modules.color import paint_groups
    font = CurrentFont()
    paint_groups(font)

### named_colors

A dictionary with color names and their corresponding color values, as `(R,G,B,alpha)` tuples.

    from hTools2.modules.color import named_colors
    print named_colors.keys()

    >>> ['blue', 'purple', 'pink', 'green', 'yellow', 'orange', 'cyan', 'red']

    print named_colors['orange']

    >>> (1, 0.66, 0.0, 1)

### solarized_colors

Solarized colors by name and `(R,G,B)` values.

    from hTools2.modules.color import solarized_colors
    print solarized_colors.keys()

    >>> ['blue', 'base01', 'base00', 'base03', 'base02', 'yellow', 'base0', 'base1', 'base2', 'base3', 'green', 'violet', 'orange', 'cyan', 'magenta', 'red']

### solarized_groups

Solarized colors by name, divided into groups.

    from hTools2.modules.color import solarized_groups
    print solarized_groups.keys()

    >>> ['dark', 'content', 'colors', 'bright']

### solarized_color(color_name)

Return a `(R,G,B)` color for a given `color_name` in the solarized palette.

    from hTools2.modules.color import solarized_color
    print solarized_color('green')

    >>> (133, 152, 0)

    print solarized_color('base01')

    >>> (88, 110, 117)

### x11_colors

X11 colors by name and `(R,G,B)` values.

    from hTools2.modules.color import x11_colors
    print x11_colors.keys()

    >>> ['Pink', 'Blue', 'Honeydew', 'Purple', 'Fuchsia', 'LawnGreen', 'AliceBlue', 'Crimson', 'White', 'NavajoWhite', 'Cornsilk', ..., 'LightPink', 'MediumAquamarine', 'OldLace']

### x11_groups

X11 colors by name, divided in groups.

    from hTools2.modules.color import x11_groups
    print x11_groups.keys()

    >>> ['pink', 'blue', 'brown', 'purple', 'yellow', 'gray', 'green', 'orange', 'white', 'red']

### x11_color(color_name)

Return a `(R,G,B)` color for a given `color_name` in the X11 palette.

    from hTools2.modules.color import x11_color
    print x11_color('Aquamarine')

    >>> (127, 255, 212)

    print x11_color('PapayaWhip')

    >>> (255, 239, 213)
