# [h] hTools2.modules.nodebox

'''
hTools2.modules.nodebox
=======================

Functions
---------

### `draw_horizontal_line(Y, context, stroke_=None, color_=None)`

Draws an horizontal line at vertical position `y` in `context`. Also accepts optional `stroke_` and `color_` parameters.

    from hTools2.modules.nodebox import draw_horizontal_line
    draw_horizontal_line(353, _ctx, stroke_=26, color_=color(0, 1, 0))

### `draw_vertical_line(x, context, stroke_=None, color_=None, y_range=None)`

Draws a vertical line at horizontal position `x` in `context`. Also accepts optional `stroke_` and `color_` parameters.

    from hTools2.modules.nodebox import draw_vertical_line
    draw_vertical_line(73, _ctx, stroke_=22, color_=color(1, 0, 0))

### `draw_cross((x, y), context, size_=10, stroke_=None, color_=None)`

Draws a cross at position `(x,y)`. Also accepts the optional parameters `size_`, `color_` and `size_`.

    from hTools2.modules.nodebox import draw_cross
    draw_cross((30, 50), _ctx, size_=20, stroke_=2, color_=color(0, 0, 1))

### `draw_grid(context, pos=(0,0), size_=1)`

Draws a grid in `context`. The optional parameters `pos` and `size` control the start of the grid and the size of the grid cells.

    from hTools2.modules.nodebox import draw_grid
    draw_grid(_ctx, pos=(20, 50), size_=10)

### `gridfit((x, y), grid)`

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

### `capstyle(path, style)`
	
Sets the `capstyle` for the given `path`, and returns the modified result.

The available options are: `0=butt`, `1=round` and `2=square`.

### `joinstyle(path, style)`

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

### `make_string(glyph_names, spacer=None)`

Makes a string of text from a list of `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.

    from hTools2.modules.nodebox import make_string
    glyph_names = [ 'o', 'l', 'aacute', 'exclam' ]
    print make_string(glyph_names)

    >>> olá!

    print make_string(glyph_names, spacer='.')

    >>> .o.l.á.!. 

### `make_string_names(glyph_names, spacer=None)`

Makes a string of slash-separated `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.

    from hTools2.modules.nodebox import make_string_names
    glyph_names = [ 'o', 'l', 'aacute', 'exclam' ]
    print make_string_names(glyph_names)

    >>> /o/l/aacute/exclam

    print make_string_names(glyph_names, spacer='period')

    >>> /o/period/l/period/aacute/period/exclam/period

### `draw_glyph(name, ufo_path, (x, y), context, _color=None, _scale=1)`

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

'''

from random import random

from AppKit import NSFontManager

from fontTools.pens.basePen import BasePen
from robofab.world import RFont

from hTools2.modules.pens import NodeBoxPen
from hTools2.modules.encoding import unicode2psnames

def draw_horizontal_line(Y, ctx, stroke_=None, color_=None):
	_stroke = 1
	_color = ctx.color(0, 1, 1)
	if stroke_ is not None:
		_stroke = stroke_
	if color_ is not None:
		_color = color_
	ctx.stroke(_color)
	ctx.strokewidth(_stroke) 
	ctx.line(0, Y + .5, ctx.WIDTH, Y + .5)

def draw_vertical_line(x, ctx, stroke_=None, color_=None, y_range=None):
	_stroke = 1
	_color = ctx.color(0, 1, 1)
	if stroke_ is not None:
		_stroke = stroke_
	if color_ is not None:
		_color = color_
	if y_range is not None:
		y_min, y_max = y_range
	else:
		y_min = 0
		y_max = ctx.HEIGHT
	ctx.stroke(_color)
	ctx.strokewidth(_stroke)
	x += .5
	ctx.line(x, y_min, x, y_max)

def draw_cross((x, y), ctx, size_=10, stroke_=None, color_=None):
	cross = size_
	_stroke = 1
	_color = ctx.color(.25)
	if stroke_ is not None:
		_stroke = stroke_
	if color_ is not None:
		_color = color_
	ctx.push()
	ctx.stroke(_color)
	ctx.strokewidth(_stroke)
	ctx.fill(None)
	x += .5
	y += .5
	ctx.line(x -cross, y, x + cross, y)
	ctx.line(x, y - cross, x, y + cross)
	ctx.pop()

def draw_grid(ctx, pos=(0,0), size_=1, stroke_=None, color_=None):
	x, y = pos
	_stroke = 1
	_color = ctx.color(.25)
	if stroke_ is not None:
		_stroke = stroke_
	if color_ is not None:
		_color = color_
	# draw lines
	ctx.stroke(_color)
	ctx.strokewidth(_stroke)
	ctx.fill(None)
	for i in range(ctx.HEIGHT / size_):
		ctx.line(0, y + .5, ctx.WIDTH, y + .5)
		y += size_
	for j in range(ctx.WIDTH / size_):
		ctx.line(x + .5, 0, x + .5, ctx.HEIGHT)
		x += size_

def gridfit((x, y), grid):
	x = (x // grid) * grid
	y = (y // grid) * grid
	return (int(x), int(y))

# http://nodebox.net/code/index.php/shared_2007-10-27-14-54-26

def capstyle(path, style):
	# 0 : butt
	# 1 : round
	# 2 : square
	path._nsBezierPath.setLineCapStyle_(style)
	return path
	
def joinstyle(path, style): 
	# 0 : miter
	# 1 : round
	# 2 : bevel
	path._nsBezierPath.setLineJoinStyle_(style)
	return path

def make_string(names_list, spacer=None):
	if spacer is not None:
		_spacer = spacer
	else:
		_spacer = ''
	_string = _spacer
	for glyph_name in names_list:
		for k in unicode2psnames.keys():	
			if unicode2psnames[k] == glyph_name:
				char = unichr(k)
				_string = _string + char + _spacer
			else:
				continue
	return _string

def make_string_names(names_list, spacer=None):
	if spacer is not None:
		_spacer = '/' + spacer
	else:
		_spacer = ''
	_glyph_names = ''
	for glyph_name in names_list:
		_glyph_names = _glyph_names + '/' + glyph_name + _spacer
	return _glyph_names

def all_glyphs(groups, spacer=None):
	all_glyphs = ""
	skip = ['invisible']
	for group_name in groups.keys():
		if group_name in skip:
			pass
		else:
			glyph_names_list = groups[group_name]
			all_glyphs += make_string(glyph_names_list, spacer)
	return all_glyphs

def draw_glyph(glyph_name, ufo_path, (x, y), context, _color=None, _scale=1):
	_ufo = RFont(ufo_path)
	_pen = NodeBoxPen(_ufo._glyphSet, context)
	_units_per_em = _ufo.info.unitsPerEm
	_units_per_element = 64
	_ppem = _units_per_em / _units_per_element
	# draw glyph outline
	context.stroke(None)
	if _color is not None:
		context.fill(_color)
	g = _ufo[glyph_name]
	context.push()
	context.transform(mode='CORNER')
	context.translate(x, y)
	context.scale(_scale)
	context.beginpath()
	g.draw(_pen)
	P = context.endpath(draw=False)
	context.drawpath(P)
	context.pop()

def glyph_metrics(gName, ufo_path, (x, y), _scale=1, _print=False):
	_ufo = RFont(ufo_path)
	_units_per_element = 64
	g = _ufo[gName]
	# get glyph & font info
	_font_info = {}
	_font_info['width'] = (g.width / _units_per_element) * _scale
	_font_info['xHeight'] = (_ufo.info.xHeight / _units_per_element) * _scale
	_font_info['capHeight'] = (_ufo.info.capHeight / _units_per_element) * _scale
	_font_info['descender'] = (_ufo.info.descender /_units_per_element) * _scale
	_font_info['ascender'] = (_ufo.info.ascender / _units_per_element) * _scale
	if _print:
		for k in _font_info.keys():
			print k, _font_info[k]
	return _font_info
	
def make_alpha(res):
    factor = (1.0 / res)
    alpha = .7 - (factor * .3)    
    return alpha

def local_fonts():
    return NSFontManager.sharedFontManager().availableFonts()
