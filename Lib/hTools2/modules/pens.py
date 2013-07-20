# [h] hTools2.modules.pens

'''Pens for drawing glifs in various environments.'''

from fontTools.pens.basePen import BasePen

try:
    from mojo.drawingTools import *
except:
    pass

class RoboFontPen(BasePen):

    '''A pen to draw a glyph on a RoboFont canvas.'''

    def __init__(self, glyphset):
        BasePen.__init__(self, glyphset)

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

    '''A pen to draw a glyph on a NodeBox canvas.'''

    def __init__(self, glyphSet, ctx, strokefont=False):
        self.ctx = ctx
        self.strokefont = strokefont
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
        if self.strokefont is False:
            self.ctx.closepath()
