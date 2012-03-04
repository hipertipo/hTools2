# hTools2.modules.nodebox

from random import random

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

def draw_grid(ctx, pos=(0,0), size_=1):
	x, y = pos
	# defaults
	ctx.strokewidth(1)
	ctx.stroke(.9)
	# draw lines
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
