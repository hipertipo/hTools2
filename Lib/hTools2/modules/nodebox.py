# hTools2.modules.nodebox

from random import random

from robofab.world import RFont
from fontTools.pens.basePen import BasePen

class NodeBoxPen(BasePen):

	'''a pen to draw .glyfs in a NodeBox canvas'''

	def __init__(self, glyphSet, context):
		self.ctx = context 
		BasePen.__init__(self, glyphSet)

	F = 1 /float(125)

	def _moveTo(self, pt):
		x, y = pt
		self.ctx.moveto(x*self.F, -y*self.F)

	def _lineTo(self, pt):
		x, y = pt
		self.ctx.lineto(x*self.F, -y*self.F)
		
	def _curveToOne(self, pt1, pt2, pt3):
		x1, y1 = pt1
		x2, y2 = pt2
		x3, y3 = pt3
		self.ctx.curveto(x1*self.F, y1*self.F, x2*self.F, y2*self.F, x3*self.F, y3*self.F)

	def _closePath(self):
		self.ctx.closepath()

def drawHorzLine(Y, ctx, s=None, c=None):
	_s = .35
	_c = ctx.color(0, 1, 1)
	if s is not None: _s = s
	if c is not None: _c = c
	ctx.stroke(_c)
	ctx.strokewidth(_s) 
	ctx.line(0, Y, ctx.WIDTH, Y)

def drawVertLine(X, ctx, s=None, c=None):
	_s = .35
	_c = ctx.color(0, 1, 1)
	if s is not None: _s = s
	if c is not None: _c = c
	ctx.stroke(_c)
	ctx.strokewidth(_s) 
	ctx.line(X, 0, X, ctx.HEIGHT)

def drawCross((x, y), ctx, _size=10, _strokewidth=None, _strokecolor=None):
	cross = _size
	_s = .5
	_c = ctx.color(.25)
	if _strokewidth is not None:
		_s = _strokewidth
	if _strokecolor is not None:
		_c = _strokecolor
	ctx.push()
	ctx.stroke(_c)
	ctx.strokewidth(_s)
	ctx.fill(None)
	ctx.line(x - cross, y, x + cross, y)
	ctx.line(x, y - cross, x, y + cross)
	ctx.pop()

def drawGrid(ctx, pos=(0,0), _size=1):
	x, y = pos
	# drawing defaults
	ctx.strokewidth(.5)
	ctx.stroke(0, 1, 1, .5)
	# draw lines
	for i in range(ctx.HEIGHT/_size):
		ctx.line(0, y, ctx.WIDTH, y)
		y += _size
	for j in range(ctx.WIDTH/_size):
		ctx.line(x, 0, x, ctx.HEIGHT)
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


def makeString(gNamesList, spacer=None):
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

def makeStringNames(gNamesList, spacer=None):
	if spacer is not None:
		_spacer = '/' + spacer
	else:
		_spacer = ''
	_gNames = ''
	for gName in gNamesList:
		_gNames = _gNames + '/' + gName + _spacer
	return _gNames

def allGlyphs(groups, spacer=None):
	allGlyphs = ""
	skip = ['invisible']
	for groupName in groups.keys():
		if groupName in skip:
			pass
		else:
			gNamesList = groups[groupName]
			allGlyphs += makeString(gNamesList, spacer)
	return allGlyphs

def drawGlyph(gName, ufo_path, (x, y), context, gridsize, _color=None):
	_ufo = RFont(ufo_path)
	_pen = NodeBoxPen(_ufo._glyphSet, context)
	_units_per_element = 125
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
	context.scale(gridsize)
	context.beginpath()
	g.draw(_pen)
	P = context.endpath(draw=False)
	context.drawpath(P) 
	context.pop()	 
	# get glyph & font info
	_font_info = {}
	_font_info['width'] = x + ((g.width / _units_per_element) * gridsize)
	_font_info['xHeight'] = y - ((_ufo.info.xHeight / _units_per_element) * gridsize)
	_font_info['capHeight'] = y - ((_ufo.info.capHeight / _units_per_element) * gridsize)
	_font_info['descender'] = y - ((_ufo.info.descender / _units_per_element) * gridsize)
	_font_info['ascender'] = y - ((_ufo.info.ascender / _units_per_element) * gridsize)
	return _font_info

