# [h] hTools.modules.pens

'''
hTools.modules.pens
===================

Objects
-------

### RoboFontPen(BasePen)

A pen to draw a glyph on a RoboFont canvas.

### NodeBoxPen(BasePen)

A pen to draw a glyph on a NodeBox canvas.

    from robofab.world import RFont
    from hTools2.modules.pens import NodeBoxPen

    ufo_path = u"/fonts/_Publica/_ufos/Publica_55.ufo"
    ufo = RFont(ufo_path)
    pen = NodeBoxPen(ufo, _ctx)
    g = ufo['a']
    translate(11, 540)
    transform('CORNER')
    scale(97 * .01)
    fill(.9)
    stroke(.5)
    strokewidth(226 * .01)
    beginpath()
    g.draw(pen)
    p = endpath(draw=False)
    drawpath(p)

    # http://nodebox.net/code/index.php/Manipulating_Paths
    nostroke()
    oval_size = 10
    for point in p:
        x = point.x - (oval_size/2)
        y = point.y - (oval_size/2)
        if point.cmd == 0:
            fill(1, 0, 0)
            oval(x, y, oval_size, oval_size)
        elif point.cmd == 1:
            fill(0, 1, 0)
            oval(x, y, oval_size, oval_size)
        elif point.cmd == 2:
            fill(0, 0, 1)
            oval(x, y, oval_size, oval_size)

'''

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
