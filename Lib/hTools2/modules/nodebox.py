# hTools2.modules.nodebox

from random import random

from fontTools.pens.basePen import BasePen
from robofab.world import RFont

from hTools2.modules.pens import NodeBoxPen

def draw_horizontal_line(Y, ctx, s=None, c=None):
	_s = 1
	_c = ctx.color(0, 1, 1)
	if s is not None:
		_s = s
	if c is not None:
		_c = c
	ctx.stroke(_c)
	ctx.strokewidth(_s) 
	ctx.line(0, Y+.5, ctx.WIDTH, Y+.5)

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

def draw_cross((x, y), ctx, _size=10, _strokewidth=None, _strokecolor=None):
	cross = _size
	_s = 1
	_c = ctx.color(.25)
	if _strokewidth is not None:
		_s = _strokewidth
	if _strokecolor is not None:
		_c = _strokecolor
	ctx.push()
	ctx.stroke(_c)
	ctx.strokewidth(_s)
	ctx.fill(None)
	x += .5
	y += .5
	ctx.line(x -cross, y, x + cross, y)
	ctx.line(x, y - cross, x, y + cross)
	ctx.pop()

def draw_grid(ctx, pos=(0,0), _size=1):
	x, y = pos
	# drawing defaults
	ctx.strokewidth(1)
	ctx.stroke(.9)
	# draw lines
	for i in range(ctx.HEIGHT/_size):
		ctx.line(0, y+.5, ctx.WIDTH, y+.5)
		y += _size
	for j in range(ctx.WIDTH/_size):
		ctx.line(x+.5, 0, x+.5, ctx.HEIGHT)
		x += _size

def gridfit(x, y, grid):
	x = (x // grid) * grid
	y = (y // grid) * grid
	return (int(x), int(y))

def capstyle(path, style): 
	path._nsBezierPath.setLineCapStyle_(style)
	return path
	
def joinstyle(path, style): 
	path._nsBezierPath.setLineJoinStyle_(style)
	return path

def make_string(gNamesList, spacer=None):
	if spacer is not None:
		_spacer = spacer
	else:
		_spacer = ''
	_string = _spacer
	for gName in gNamesList:
		for k in unicode2psnames.keys():	
			if unicode2psnames[k] == gName:
				char = unichr(k)
				_string = _string + char + _spacer
			else:
				continue
	return _string

def make_string_names(gNamesList, spacer=None):
	if spacer is not None:
		_spacer = '/' + spacer
	else:
		_spacer = ''
	_gNames = ''
	for gName in gNamesList:
		_gNames = _gNames + '/' + gName + _spacer
	return _gNames

def all_glyphs(groups, spacer=None):
	allGlyphs = ""
	skip = ['invisible']
	for groupName in groups.keys():
		if groupName in skip:
			pass
		else:
			gNamesList = groups[groupName]
			allGlyphs += makeString(gNamesList, spacer)
	return allGlyphs

def draw_glyph(gName, ufo_path, (x, y), context, _color=None, _scale=1):
	_ufo = RFont(ufo_path)
	_pen = NodeBoxPen(_ufo._glyphSet, context)
	_units_per_em = _ufo.info.unitsPerEm
	_units_per_element = 64
	_ppem = _units_per_em / _units_per_element
	# draw glyph outline
	context.stroke(None)
	if _color is not None:
		context.fill(_color)
	else:
		context.fill(1, 0, .5, .3)
	g = _ufo[gName]
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

