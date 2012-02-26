# coding=utf-8

#=============================================
# FractalTools
# L-system-based fractal shapes in NodeBox
# (c) Gustavo Ferreira, 2007
# http://hipertipo.com/

#---------------------------------------------
#  imports

from math import sin, cos, pi

from nodebox.graphics import Context
_ctx = Context()

colors = _ctx.ximport("colors")
reload(colors)

#---------------------------------------------
#  fractal shapes

fractalz = {
	'koch1' : {
		'string' :		"F+F+F+F",
		'rule1' :		( "F", "FF-F-F-F-F-F+F" ),
		'rule2' :		( None, None ),
		'angle' :		pi/2,
		'_angle' :		90,		
		},
	'koch2' : {
		'string' :		"F-F-F-F",
		'rule1' :		( "F", "F-F+F+FF-F-F+F" ),
		'rule2' :		( None, None ),
		'angle' :		pi/2,
		'_angle' :		90,		
		},
	'snowflake' : {
		'string' :		"F-F-F-F",
		'rule1' :		( "F", "F+F-F-F+F" ),
		'rule2' :		( None, None ),
		'angle' :		pi/2,
		'_angle' :		90,
		},
	'cross' : {
		'string' :		"F-F-F-F",
		'rule1' :		( "F", "F-F+F-F-F" ),
		'rule2' :		( None, None ),
		'angle' :		pi/2,
		'_angle' :		90,
		},
	'branches' : {
		'string' :		"F-F-F-F",
		'rule1' :		( "F", "FF-F--F-F" ),
		'rule2' :		( None, None ),
		'angle' :		pi/2,
		'_angle' :		90,
		},
	'dragon' : {
		'string' :		"F",
		'rule1' :		( "F", "F+G+" ),
		'rule2' :		( "G", "-F-G" ),
		'angle' :		pi/2,
		'_angle' :		90,
		},
	'sierpinsky' : {
		'string' :		"G",
		'rule1' :		( "F", "G+F+G" ),
		'rule2' :		( "G", "F-G-F" ),
		'angle' :		pi/3,
		'_angle' :		60,
		},
	'fass1' : {
		'string' :		"F",
		'rule1' :		( "F", "F+G++G-F--FF-G+" ),
		'rule2' :		( "G", "-F+GG++G+F--F-G" ),
		'angle' :		pi/3,
		'_angle' :		60,
		},
	}

def parser(string, i, rule1, rule2):
	if i > 0:
		newString = ""
		for char in string:
			if char == rule1[0]: newString = newString + rule1[1]
			elif char == rule2[0]: newString = newString + rule2[1]
			else: newString = newString + char
		return parser(newString, i-1, rule1, rule2)
	else: return string


#---------------------------------------------
# general functions

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

def markPos(x, y, gridsize, type="cross"):
	if type == "cross":
		_stroke = gridsize/10
		_ctx.push()
		_ctx.nofill()
		_ctx.stroke(CVTColors["laranja"])
		_ctx.strokewidth(_stroke)
		_ctx.line(x-gridsize, y, x+gridsize, y)
		_ctx.line(x, y-gridsize, x, y+gridsize)
		_ctx.stroke(None)
		_ctx.pop()
	if type == "oval":
		_size = gridsize/2
		_ctx.push()
		_ctx.stroke(None)
		_ctx.fill(CVTColors["laranja"])
		_ctx.oval(x-(_size/2), y-(_size/2), _size, _size)
		_ctx.pop()

def colorRange(i, iterations, colorFactor, grad=None, inv=None):
	'''calculate color value for instance of iterator + features'''
	r, g, b, t = 0, .5, 1, 1
	if grad == None:
		grad = 0,1,0,0
	if inv == None:
		inv = 0,0,0,0
	if grad[0] == 1:
		r = ( (float(i)/(iterations-1) ) ** colorFactor )
	if grad[1] == 1:
		g = ( (float(i)/(iterations-1) ) ** colorFactor )
	if grad[2] == 1:
		b = ( (float(i)/(iterations-1) ) ** colorFactor )
	if grad[3] == 1:
		t = ( (float(i+1)/(iterations-1) ) ** colorFactor )
	if inv[0] == 1:
		r = 1-r
	if inv[1] == 1:
		g = 1-g
	if inv[2] == 1:
		b = 1-b
	if inv[3] == 1:
		t = 1-t		
	return r, g, b, t

#---------------------------------------------

CVTColors = {
	"ciano" : colors.cmyk(100, 0, 0, 0, range=100),
	"azul-claro" : colors.cmyk(80, 30, 0, 0, range=100),
	"azul" : colors.cmyk(100, 100, 0, 0, range=100),
	"azul-escuro" : colors.cmyk(90, 80, 0, 20, range=100),
	"laranja" : colors.rgb(255, 51, 0, range=255),
	}

#---------------------------------------------
# objects

class Page:

	def __init__(self, _size, grid, drawGrid=True, neg=False, mono=False):
		self.w, self.h = _size
		self.grid = grid
		self.neg = neg
		self.mono = mono
		self.drawGrid = drawGrid
		self.draw()

	def _drawCanvas(self):
		if self.neg == True and self.mono == False:
			bgColor = CVTColors["azul-escuro"]
		elif self.neg == True and self.mono ==True:
			bgColor = _ctx.color(0)
		else:
			bgColor = _ctx.color(1)
		_ctx.background(_ctx.color(bgColor))
		_ctx.size(self.w, self.h)

	def _drawGrid(self):
		columns = int( self.w / self.grid )
		rows = int( self.h / self.grid )
		_ctx.push()
		_ctx.nofill()
		_ctx.strokewidth(1)
		# set guideline color according to background
		if self.neg == False and self.mono == False:
			_ctx.stroke(_ctx.color(0, 0, 1, .25))
		elif self.neg == False and self.mono == True:
			_ctx.stroke(_ctx.color(0, 0, 0, .15))
		elif self.neg == True and self.mono == False:
			_ctx.stroke(_ctx.color(0, 0, 1, .75))
		elif self.neg == True and self.mono == True:
			_ctx.stroke(_ctx.color(1, 1, 1, .15))
		else:
			_ctx.stroke(_ctx.color(0, 0, 1, .5))
		# draw gridline
		for c in range(columns-1):
			_ctx.line((c+1)*self.grid, 0, (c+1)*self.grid, self.h)
		for r in range(rows-1):
			_ctx.line(0, (r+1)*self.grid, self.w, (r+1)*self.grid)
		_ctx.pop()

	def draw(self):
		self._drawCanvas()
		if self.drawGrid == True: self._drawGrid()

#---------------------------------------------

class LFractal:
	
	angle = 0
	strokeWidth = 3.0
	strokeColor = CVTColors["azul-claro"]
	lineCap = 1
	lineJoin = 1
	fillColor = None
	autoClose = False
	markPos = False
	axis = False
	drawPoints = False

	def __init__(self, pos, levels, grid, name="dragon", alignToGrid=True):
		self.grid = grid
		self.string = fractalz[name]['string']
		self.angleStep = fractalz[name]['angle']
		self.rule1 = fractalz[name]['rule1']
		self.rule2 = fractalz[name]['rule2']
		if fractalz[name].has_key('rule3'):
			self.rule3 = fractalz[name]['rule3']
		self.set(pos, levels, alignToGrid)
		self.parse()
		
	def set(self, pos, levels, alignToGrid):
		self.levels = levels
		self.strokeWidth = (self.strokeWidth/10) * self.grid
		self.x, self.y = pos
		if alignToGrid == True: self.x, self.y = gridfit(self.x, self.y, self.grid)
		self.xMin, self.yMin = self.x, self.y
		self.xMax, self.yMax = self.x, self.y
		
	def parse(self):
		self.pString = parser(self.string, self.levels, self.rule1, self.rule2)

	def measure(self, x, y):
		xMin, yMin, xMax, yMax = 0, 0, 0, 0
		if x < self.xMin:
			self.xMin = x
		if x > self.xMax:
			self.xMax = x
		if y < self.yMin:
			self.yMin = y
		if y > self.yMax:
			self.yMax = y
		
	def forward(self):
		x1 = self.x + cos(self.angle) * self.grid
		y1 = self.y + sin(self.angle) * self.grid
		_ctx.lineto(x1, y1)
		self.x, self.y = x1, y1
		self.measure(self.x, self.y)

	def left(self):
		angle1 = self.angle - self.angleStep
		self.angle = angle1
		self.measure(self.x, self.y)

	def right(self):
		angle1 = self.angle + self.angleStep
		self.angle = angle1
		self.measure(self.x, self.y)

	def setState(self, strokeColor, autoClose, strokeWidth, fillColor, _shadow):
		_ctx.stroke(_ctx.color(strokeColor))
		_ctx.strokewidth(strokeWidth)
		_ctx.autoclosepath(autoClose)
		_ctx.fill(_ctx.color(fillColor))
		if _shadow != None:
			colors.shadow(_shadow['dx'], _shadow['dy'], _shadow['alpha'], _shadow['blur'])

	def draw(self, strokeColor=None, autoClose=None, strokeWidth=None, fillColor=None, \
		lineCap=None, lineJoin=None, markPosition=None, axis=None, box=False, drawPoints=None, shadow=None):
		'''draw fractal shape using given parameters'''
		# if no parameters use defaults
		if strokeColor == None:
			strokeColor = self.strokeColor
		if autoClose == None:
			autoClose = self.autoClose
		if strokeWidth == None:
			strokeWidth = self.strokeWidth
		if fillColor == None:
			fillColor = self.fillColor
		if lineCap == None:
			lineCap = self.lineCap
		if lineJoin == None:
			lineJoin = self.lineJoin
		if markPosition == None:
			markPosition = self.markPos
		if drawPoints == None:
			drawPoints = self.drawPoints
		if axis == None:
			axis = self.axis
		self.setState(strokeColor, autoClose, strokeWidth, fillColor, shadow)
		# initialize drawing 
		i = 0
		self.x0, self.y0 = self.x, self.y
		_ctx.beginpath()
		_ctx.moveto(self.x, self.y)
		# calculate fractal path 
		for char in self.pString:
			if char == "F": self.forward()
			elif char == "G": self.forward()
			elif char == "f": self.forward()		
			elif char == "+": self.left()
			elif char == "-": self.right()
			else: continue
			i = i + 1
		###x2, y2 = self.x, self.y
		# get width & height
		self.height = ( self.yMax - self.yMin ) / self.grid
		self.width = ( self.xMax - self.xMin ) / self.grid
		# draw fractal path on canvas
		p = _ctx.endpath()
		capstyle(p, lineCap)
		joinstyle(p, lineJoin)
		_ctx.drawpath(p)
		# mark position
		if markPosition == True:
			markPos(self.x0, self.y0, self.grid)
		# draw point
		if drawPoints == True:
			markPos(self.x0, self.y0, self.grid, type="oval")
			markPos(self.x, self.y, self.grid, type="oval")
		# draw axis
		if axis == True:
			_ctx.push()
			_ctx.nofill()
			_ctx.stroke(CVTColors["laranja"])
			_ctx.strokewidth(2)
			_ctx.line(self.x0, self.y0, self.x, self.y)
			_ctx.pop()
			# calculate axis length
			### print self.x0-self.x, self.y0-self.y # ...
		# draw box
		if box == True:
			_ctx.push()
			_ctx.nofill()
			_ctx.strokewidth(1)
			_ctx.stroke(CVTColors["laranja"])
			_ctx.rect(self.xMin, self.yMin, self.width*self.grid, self.height*self.grid)
			_ctx.pop()

#---------------------------------------------

class FractalColors:
	
	def __init__( self, (x, y), iterations, grid, colorFactor, colorsList=None, name="dragon", \
		strokeWidth=None, barPos=(0,0), barSettings=((2,2),1), shadow=None ):
		self.grid = grid
		self.x, self.y = x, y
		self.name = name
		self.iterations = iterations
		self.factor = colorFactor
		self.strokeWidth = strokeWidth
		self.barPos = barPos
		self.barSize, self.barSpacing = barSettings
		self.shadow = shadow
		# colors
		if colorsList != None:
			self.colorsList = colorsList
		else:
			self.colorsList = CVTColors["ciano"], CVTColors["azul"]
		# min / max
		self.xMin, self.yMin = self.x, self.y
		self.xMax, self.yMax = self.x, self.y

	def draw(self, showInfo=False, _markPosition=False, _drawPoints=False, _axis=False, box=False, mono=False, vShift=None, hShift=None):
		# color calibration bar 
		if showInfo != False:
			c = ColorBar(self.barPos, self.iterations, self.factor, self.grid, colorsList=self.colorsList, showInfo=showInfo).draw(self.barSize, self.barSpacing)
		# calculate colors
		if mono != False:
			g = colors.gradient([_ctx.color(.8), _ctx.color(.2)], steps=self.iterations, spread=self.factor)
		else:
			g = colors.gradient(self.colorsList, steps=self.iterations, spread=self.factor)
		# draw
		for i in range(len(g)):
			# reverse order = draw biggest first
			L = self.iterations-i-1
			# create fractal object
			F = LFractal((self.x, self.y), L, self.grid, self.name, alignToGrid=True)
			# set stroke
			F.strokeColor = g[i]
			if self.strokeWidth != None: F.strokeWidth = self.strokeWidth
			# the biggest one
			if L == self.iterations-1:
				# turn shadow on
				if self.shadow != None: colors.shadow(self.shadow['dx'], self.shadow['dy'], self.shadow['alpha'], self.shadow['blur'])
				# draw the biggest fractal on canvas (box)
				F.draw(markPosition=_markPosition, drawPoints=_drawPoints, axis=_axis, box=box)
				# get height & width for set
				self.height, self.width = F.height, F.width
				# turn shadow off
				if self.shadow != None: colors.noshadow()
			# all other levels
			else: F.draw(markPosition=_markPosition, drawPoints=_drawPoints, axis=_axis, box=False)
			# the shifters
			if hShift != None:
				self.x = F.x + hShift
			if vShift != None:
				self.y = F.y + vShift
			
#---------------------------------------------

class ColorBar:

	_font = "Verdana"
	_fontSize = 13
	_fontColor = .5

	def __init__(self, (x,y), steps, factor, grid, colorsList=None, showInfo=None):
		self.x, self.y = x, y
		self.steps = steps
		self.factor = factor
		self.grid = grid
		if colorsList != None: self.colorsList = colorsList
		else: self.colorsList = CVTColors["ciano"], CVTColors["azul"]

	def drawGlobalInfo(self, x=50, y=50):
		_ctx.fill(self._typeColor)
		_ctx.font(self._font)		
		_ctx.fontsize(self._fontSize)
		info = "iterations: %s	factor: %s" % ( self.steps, self.factor )
		_ctx.text(info, x, y)

	def drawColors(self, (w, h), spacing, alignToGrid, markPosition):
		# align to grid
		if alignToGrid == True:
			x, y = gridfit(self.x, self.y, self.grid)
		else: x, y = self.x, self.y
		# mark position
		if markPosition == True: markPos(x, y, self.grid)
		# calculate colors
		G = colors.gradient(self.colorsList, steps=self.steps, spread=self.factor)
		# draw swatches
		for i in range(len(G)):
			_ctx.nostroke()
			_ctx.fill(G[i])
			X, Y = x, y + (((h + spacing) * self.grid) * i)
			# draw swatch
			_ctx.rect(X, Y, w * self.grid, h * self.grid)

	def draw(self, (w, h), spacing, alignToGrid=True, markPosition=True):
		### _ctx.nostroke()
		### self.drawGlobalInfo()
		self.drawColors((w, h), spacing, alignToGrid, markPosition)

#-----------------------------------------------------------------------

class Texto:

	txt = u"Centro Vocacional Tecnológico"
	fontName = "Verdana-Bold"
	
	def __init__(self, (x, y), grid, factor=1, horizontal=False, alignToGrid=True, markPosition=False, fillColor=None):
		self.x, self.y = x, y
		self.grid = grid
		self.factor = factor
		self.fontSize = grid * factor * 0.9
		self.horizontal = horizontal
		self.alignToGrid = alignToGrid
		self.markPosition = markPosition
		if fillColor != None:
			self.fillColor = fillColor
		else: self.fillColor = CVTColors["azul-escuro"]
		self.draw()

	def draw(self):
		_ctx.font(self.fontName)
		_ctx.fontsize(self.fontSize)
		_ctx.fill(self.fillColor)
		# align to grid
		if self.alignToGrid == True:
			x, y = gridfit(self.x, self.y, self.grid)
		else:
			x, y = self.x, self.y
		# cache position
		x0, y0 = x, y
		# compact version
		if self.horizontal == False:
			words = self.txt.split(' ')
			for word in words:
				_ctx.text(word, x, y)
				y += self.grid
		# horizontal version
		else:
			_ctx.text(self.txt, x, y)
		# mark position
		if self.markPosition == True:
			markPos(x0, y0, self.grid)

#-----------------------------------------------------------------------

class CVTsMarca:
	
	def __init__(self, (x, y), levels, grid, horizontal=False, alignToGrid=True, markPosition=False, drawText=True, negative=False, mono=False):
		self.x, self.y = x, y
		self.levels = levels
		self.grid = grid
		self.horizontal = horizontal
		self.alignToGrid = alignToGrid
		self.markPosition = markPosition
		self.drawText = drawText
		self.negative = negative
		self.mono = mono
		self.draw()
		
	def draw(self):
		if self.alignToGrid == True: self.x, self.y = gridfit(self.x, self.y, self.grid)
		# positivo / cor
		if self.negative == False and self.mono == False:
			self.drawType() 
			self.drawFractal()
		# negativo / cor
		elif self.negative == True and self.mono == False:
			self.drawType(tColor=_ctx.color(1))
			self.drawFractal()
		# positivo / pb
		elif self.negative == False and self.mono == True:
			self.drawType(tColor=_ctx.color(0))
			self.drawFractal(fColor=_ctx.color(0))
		# negativo / pb
		elif self.negative == True and self.mono == True:
			self.drawType(tColor=_ctx.color(1))
			self.drawFractal(fColor=_ctx.color(1))

	def drawFractal(self, fColor=None):
		f = LFractal((self.x, self.y), self.levels, self.grid, alignToGrid=False)
		if fColor != None: f.strokeColor = fColor
		f.draw()

	def drawType(self, tColor=None):
		d = self.grid
		if self.levels < 5 :
			print "iterações menores que 5 não possuem tipo"
		elif self.levels > 7 :
			print "iterações maiores que 7 não possuem tipo"
		else: 
			# 5 iterations
			if self.levels == 5:
				x, y = self.x+d, self.y+(d*4) 
				linespacing = d*2
				if self.horizontal == False: factor = 1
				else: factor = 1.2
			# 6 iterations
			elif self.levels == 6:
				linespacing = d*3
				if self.horizontal == False:
					x, y = self.x+(d*4), self.y-(d*2)
					factor = .95
				else:
					x, y = self.x+(d*4), self.y-(d*-3)
					factor = 1.2
			# 7 iterations
			elif self.levels == 7:
				linespacing = d*4
				if self.horizontal == False:
					x, y = self.x+(d*4), self.y-(d*8)
					factor = 1
				else:
					x, y = self.x+(d*4), self.y-(d*0)
					factor = 1.3
			# draw!
			t = Texto((x, y), linespacing, factor, self.horizontal, alignToGrid=False, fillColor=tColor)
			# mark position			
			if self.markPosition == True:
				markPos(self.x, self.y, self.grid)
				markPos(x, y, self.grid)

	def drawBox(self):
		_ctx.stroke(CVTColors["laranja"])
		_ctx.rect(self.x, self.y, 100, 100)