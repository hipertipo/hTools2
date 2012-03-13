# hTools.modules.pens

from fontTools.pens.basePen import BasePen

try:
	from mojo.drawingTools import *
except:
	pass

class RoboFontPen(BasePen):

	def __init__(self, glyphSet):
		BasePen.__init__(self, glyphSet)

	def _moveTo(self, pt):
		x, y = pt
		moveTo((x, y))

	def _lineTo(self, pt):
		x, y = pt
		lineTo((x, y))
	
	def _curveToOne(self, pt1, pt2, pt3):
		x1, y1 = pt1
		x2, y2 = pt2
		x3, y3 = pt3
		curveTo((x1, y1), (x2, y2), (x3, y3))

	def _closePath(self):
		closePath()

class NodeBoxPen(BasePen):

	def __init__(self, glyphSet, context):
		self.ctx = context 
		BasePen.__init__(self, glyphSet)

	def _moveTo(self, pt):
		x, y = pt
		self.ctx.moveto(x, -y)

	def _lineTo(self, pt):
		x, y = pt
		self.ctx.lineto(x, -y)
		
	def _curveToOne(self, pt1, pt2, pt3):
		x1, y1 = pt1
		x2, y2 = pt2
		x3, y3 = pt3
		self.ctx.curveto(x1, -y1, x2, -y2, x3, -y3)

	def _closePath(self):
		self.ctx.closepath()
