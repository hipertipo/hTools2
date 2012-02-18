colors = ximport("colors")

from robofab.world import RFont
from fontTools.pens.basePen import BasePen

from hTools.tools.ETools import EWorld, EFont, ESpace
from hTools.tools.EncodingTools import unicode2psnames
from hTools.tools.ETools_NodeBoxTools import NodeBoxPen, ELine, EParagraph

#-------------------------------------------------

class EDiagram(ESpace):
	
	tmpX = 0
	tmpY = 0
	# canvas
	canvasWidth = 800
	canvasHeight = 600
	marginX = 10
	marginY = 5
	canvasColor = colors.cmyk(0, 0, 1, 0)
	# paragraph
	eSize = 1
	txt = "Elementar"
	# cells
	cellMarginX = 5
	cellMarginY = 5
	cellColor = colors.rgb(1, 1, 1)
	cellVar = True
	# labels
	labelMarginX = 5
	labelMarginY = 5
	labelColor = colors.rgb(1, 1, 1)
	labelVar = False
	# sample
	sampleMarginX = 5
	sampleMarginY = 5
	sampleColor = colors.rgb(1, 1, 1)
	sampleVar = False

	def __init__(self, ctx):
		ESpace.__init__(self)
		self.ctx = ctx
		
	def setAxes(self, xlabel, ylabel, offset):

		# xAxis
		self.xAxis = xlabel
		self.xValues = self.parameters[xlabel]
		#self.xStep = (self.xSize - ((len(self.xValues)-1) * offset)) / len(self.xValues)
		#self.xOffset = offset

		# yAxis
		self.yAxis = ylabel
		self.yValues = self.parameters[ylabel]
		#self.yStep = (self.ySize - ((len(self.yValues)-1) * offset)) / len(self.yValues)
		#self.yOffset = offset

	def _compileDict(self, parametersDict):
		style = parametersDict["style"]
		height = parametersDict["height"]
		weight = parametersDict["weight"]
		width = parametersDict["width"]
		fontname = "E%s%s%s%sA" % ( style, height, weight, width )
		return fontname

	def compileInstance(self, xParam, yParam):
		parametersDict = {}
		for parameter in self.parameters.keys():
			if parameter == self.xAxis:
				parametersDict[parameter[:-1]] = xParam
			elif parameter == self.yAxis:
				parametersDict[parameter[:-1]] = yParam
			else:
				parameterName = parameter[:-1]
				parametersDict[parameterName] = self.parameters[parameter][0]
		EName = self._compileDict(parametersDict)
		return EName

	def buildCoordenates(self):
		self.coordenates = []
		for i in range(len(self.yValues)): 
			for j in range(len(self.xValues)):
				eName = self.compileInstance(self.xValues[j], self.yValues[i])
				x = j
				y = i
				A = i / (float(len(self.yValues)) - 1)
				B = j / (float(len(self.xValues)) - 1)
				C = .5
				D = 1
				# size = self.xStep, self.yStep
				pos = (x, y) 
				_color = colors.rgb(A, B, C, D)
				instance = (eName, pos, _color) 
				self.coordenates.append(instance)

	def draw(self, cell=True, sample=True, label=True):
		self.drawCanvas()
		for coordenates in self.coordenates:
			if sample:
				self.drawSample_ufo(coordenates)
			#if cell:
			#	self.drawCell(coordenates)

	def drawSample_ufo(self, coordenates):
		EName = coordenates[0]
		x, y = coordenates[1]
		X = self.marginX + (x*self.tmpX)
		Y = self.marginY + (y*self.tmpY)
		if EName in self.ufoNames:
			P = EParagraph(EName, self.ctx)
			P.pWidth = 120
			P.txt = self.txt
			if self.sampleVar == True: 
				P.c = coordenates[2]
			else:
				P.c = self.sampleColor
			P.draw((X, Y), baseline=True)
			self.tmpX = P.pWidth
			self.tmpY = int(P.height)
		else:
			self.tmpY = int(EName[2:4])

	def drawCanvas(self):
		self.ctx.size(self.canvasWidth, self.canvasHeight)
		self.ctx.background(self.canvasColor)
		self.ctx.fill(1, 0, 1)
		
	def drawCell(self, coordenates):
		print coordenates
		x, y = coordenates[1]
		#w, h = coordenates[2]
		_color = coordenates[2]
		#t = .2
		X, Y = x+self.padding, y+self.padding
		self.ctx.fill(_color)
		self.ctx.rect(X, Y, 10, 10)

	def drawLabel(self, coordenates):
		EName = coordenates[0]
		x, y = coordenates[1]
		w, h = coordenates[2]
		if self.labelVar == True:
			r, g, b, t = coordenates[3]
			t = 1
			self.ctx.fill(r, g, b, t)
		else:
			self.ctx.fill(self.labelColor)
		X = x + self.padding + self.labelMarginX
		Y = y + self.padding + h - self.labelMarginY
		self.ctx.font("EY09112A")
		self.ctx.fontsize(8)
		self.ctx.text(EName, X, Y)


# ---------------------------------------------
# initialize EDiagram
# 

C = _ctx

d = EDiagram(C)

d.marginX = 70
d.marginY = 50
d.canvasColor = 0
#d.eSize = 2
d.styles = [ "B" ]
d.weights = [ "11" ]
d.heights = d.heights[8:]
d.widths = [ '1', '2', '3', '4', '5', ]
d.compile()
d.setAxes("widths", "heights", 0)
d.buildCoordenates()

#--- cells
d.cellMarginX = 5
d.cellMarginY = 20
d.cellVar = 1
d.cellColor = colors.rgb(1, 1, 0)

#--- labels
d.labelMarginX = 10
d.labelMarginY = 10
d.labelVar = 1
d.labelColor = colors.rgb(1, 1, 1)

#--- samples
d.sampleMarginX = 10
d.sampleMarginY = 10
d.sampleVar = 1
d.sampleColor = colors.rgb(1, 1, 1)

d.draw(cell=True, sample=True, label=True)
