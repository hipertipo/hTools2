# hTools.modules.pens

from fontTools.pens.basePen import BasePen

try:
	from mojo.drawingTools import *
except:
	print 'could not import mojo.drawingTools.\n'


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

	F = 1 / float(64) # remove scaling from pen -- move it to drawing function

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

