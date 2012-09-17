### draw\_horizontal\_line(Y, context, stroke\_=None, color\_=None)

Draws an horizontal line at vertical position `y` in `context`. Also accepts optional `stroke_` and `color_` parameters.

    from hTools2.modules.nodebox import draw_horizontal_line
    draw_horizontal_line(353, _ctx, stroke_=26, color_=color(0, 1, 0))

### draw\_vertical\_line(x, context, stroke\_=None, color\_=None, y\_range=None)

Draws a vertical line at horizontal position `x` in `context`. Also accepts optional `stroke_` and `color_` parameters.

    from hTools2.modules.nodebox import draw_vertical_line
    draw_vertical_line(73, _ctx, stroke_=22, color_=color(1, 0, 0))

### draw\_cross((x, y), context, size\_=10, stroke\_=None, color\_=None)

Draws a cross at position `(x,y)`. Also accepts the optional parameters `size_`, `color_` and `size_`.

    from hTools2.modules.nodebox import draw_cross
    draw_cross((30, 50), _ctx, size_=20, stroke_=2, color_=color(0, 0, 1))

### draw\_grid(context, pos=(0,0), size\_=1)

Draws a grid in a given `context` object.

The optional parameters `pos` and `size` control the start of the grid, and the size of the grid cells.

The optional parameter `color_` controls the color of the grid, and `mode` makes it possible to choose between two grid designs: `lines` and `dots`.

    from hTools2.modules.nodebox import draw_grid

    size(200, 200)
    background(1, 1, 0)

    gridsize = 10
    draw_grid(_ctx, size_=gridsize, pos=(2, 2), color_=color(0, 1, 0, .2), mode='lines')
    draw_grid(_ctx, size_=gridsize, pos=(6, 6), color_=color(0, 0, 1), mode='dots')

### gridfit((x, y), grid)

Takes a tuple `(x,y)` and a grid size `grid`, and returns new rounded values for `(x,y)`.

    from hTools2.modules.nodebox import *
    print gridfit((54, 58), 10)

    >>> (50, 50)

Here’s another example, using both `gridfit` and `draw_grid`.

    from hTools2.modules.nodebox import gridfit, draw_grid

    grid_size = 50
    x, y = gridfit((58, 57), grid_size)
    draw_grid(_ctx, size_=grid_size)

    stroke(None)
    for i in range(5):
        fill(random(), random(), random(), .5)
        rect(x, y, 219, 224)
        x += grid_size
        y += grid_size

### capstyle(path, style)

Sets the `capstyle` for the given `path`, and returns the modified result.

The available options are: `0=butt`, `1=round` and `2=square`.

### joinstyle(path, style)

Sets the `joinstyle` for the given `path`, and returns the modified result.

The available options are `0=miter`, `1=round` and `2=bevel`.

Here’s an example of both `capstyle` and `joinstyle` in action:

    from hTools2.modules.nodebox import *
    nofill()
    autoclosepath(False)
    stroke(0)
    strokewidth(34)
    translate(52, 49)
    beginpath(64, 38)
    lineto(241, 100)
    lineto(68, 337)
    lineto(360, 367)
    p = endpath()
    p = capstyle(p, 0)
    p = joinstyle(p, 2)
    drawpath(p)

### make_string(glyph_names, spacer=None)

Makes a string of text from a list of `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.

    from hTools2.modules.nodebox import make_string
    glyph_names = [ 'o', 'l', 'aacute', 'exclam' ]
    print make_string(glyph_names)

    >>> olá!

    print make_string(glyph_names, spacer='.')

    >>> .o.l.á.!.

### make_string_names(glyph_names, spacer=None)

Makes a string of slash-separated `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.

    from hTools2.modules.nodebox import make_string_names
    glyph_names = [ 'o', 'l', 'aacute', 'exclam' ]
    print make_string_names(glyph_names)

    >>> /o/l/aacute/exclam

    print make_string_names(glyph_names, spacer='period')

    >>> /o/period/l/period/aacute/period/exclam/period

### draw\_glyph(name, ufo\_path, (x, y), context, \_color=None, \_scale=1)

Draws the glyph with `name` from the font in `ufo_path` at position `(x,y)` in `context`.

Optionally, pass a `color` object and/or a `scale` value.

    from hTools2.modules.nodebox import draw_glyph

    ufo_path = '/fonts/_Publica/_ufos/Publica_55.ufo'
    draw_glyph('g', ufo_path, (100, 200), _ctx, _color=color(1, .5, 0), _scale=0.4)

Here is a simple glyph window with grid:

    from hTools2.modules.nodebox import *

    ufo_path = '/fonts/_Publica/_ufos/Publica_55.ufo'
    gridsize = 26
    x, y = gridfit((168, 402), gridsize)

    draw_grid(_ctx, size_=gridsize)
    draw_glyph('g', ufo_path, (x, y), _ctx, _scale=0.4)
    draw_horizontal_line(y, _ctx)
    draw_vertical_line(x, _ctx)
    draw_cross((x, y), _ctx, size_=gridsize)

