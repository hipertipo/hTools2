# [h] drawing primitives

#: constant for drawing circular arcs with beziers (thanks EvB)
BEZIER_ARC_CIRCLE = 0.5522847498

def round_int(n, d):
    """Round a number (float/int) to the closest multiple of a divisor (int)."""
    return round(n / float(d)) * d

def rect(pen, x, y, w, h):
    """Draw a rectangle with a pen object."""
    pen.moveTo( (x, y) )
    pen.lineTo( (x, y+h) )
    pen.lineTo( (x+w, y+h) )
    pen.lineTo( (x+w, y) )
    pen.closePath()

def ellipse(pen, (x, y, rx, ry)):
    """Draw an ellipse with a pen object."""
    bcpx = BEZIER_ARC_CIRCLE * rx
    bcpy = BEZIER_ARC_CIRCLE * ry
    pen.moveTo( (x, y + rx) )
    pen.curveTo( (x + bcpx, y + ry), (x + rx, y + bcpy), (x + rx, y) )
    pen.curveTo( (x + rx, y - bcpy), (x + bcpx, y - ry), (x, y - ry) )
    pen.curveTo( (x - bcpx, y - ry), (x - rx, y - bcpy), (x - rx, y) )
    pen.curveTo( (x - rx, y + bcpy), (x - bcpx, y + ry), (x, y + ry) )
    pen.closePath()

def oval(pen, x, y, w, h):
    """Draw an oval with a pen object."""
    radius_w = w / 2.0
    radius_h = h / 2.0
    bcp_w = BEZIER_ARC_CIRCLE * radius_w
    bcp_h = BEZIER_ARC_CIRCLE * radius_h
    x += radius_w
    y += radius_h
    pen.moveTo((x, y+radius_h))
    pen.curveTo((x+bcp_w, y+radius_h), (x+radius_w, y+bcp_h), (x+radius_w, y) )
    pen.curveTo((x+radius_w, y-bcp_h), (x+bcp_w, y-radius_h), (x, y-radius_h) )
    pen.curveTo((x-bcp_w, y-radius_h), (x-radius_w, y-bcp_h), (x-radius_w, y) )
    pen.curveTo((x-radius_w, y+bcp_h), (x-bcp_w, y+radius_h), (x, y+radius_h) )
    pen.closePath()

def circle(pen, x, y, size):
    """Draw a circle with a pen object."""
    oval(pen, x, y, size, size)

def square(pen, x, y, size):
    """Draw a square with a pen object."""
    rect(pen, x, y, size, size)

def element(pen, x, y, w, h, magic=BEZIER_ARC_CIRCLE):
    """Draw an element with a pen object."""
    radius_w = w * 0.5
    radius_h = h * 0.5
    bcp_w = magic * radius_w
    bcp_h = magic * radius_h
    x += radius_w
    y += radius_h
    pen.moveTo((x, y+radius_h))
    pen.curveTo((x+bcp_w, y+radius_h), (x+radius_w, y+bcp_h), (x+radius_w, y))
    pen.curveTo((x+radius_w, y-bcp_h), (x+bcp_w, y-radius_h), (x, y-radius_h))
    pen.curveTo((x-bcp_w, y-radius_h), (x-radius_w, y-bcp_h), (x-radius_w, y))
    pen.curveTo((x-radius_w, y+bcp_h), (x-bcp_w, y+radius_h), (x, y+radius_h))
    pen.closePath()

# RGlyph drawing tools

def DrawRectInGlyph(self, x, y, w, h):
    """Draw a rectangle in a glyph object."""
    pen = self.getPen()
    rect(pen, x, y, w, h)

def DrawOvalInGlyph(self, x, y, w, h):
    """Draw an oval in a glyph object."""
    pen = self.getPen()
    oval(pen, x, y, w, h)

def DrawElementInGlyph(self, x, y, w, h, magic=BEZIER_ARC_CIRCLE):
    """Draw an element in a glyph object."""
    pen = self.getPen()
    element(pen, x, y, w, h, magic)

def DrawCircleInGlyph(self, x, y, s):
    """Draw a circle in a glyph object."""
    pen = self.getPen()
    circle(pen, x, y, s)

def DrawSquareInGlyph(self, x, y, s):
    """Draw a square in a glyph object."""
    pen = self.getPen()
    square(pen, x, y, s)

def addGlyphDrawingTools(RGlyph):
    """Draw a circle in a glyph object."""
    RGlyph.rect = DrawRectInGlyph
    RGlyph.oval = DrawOvalInGlyph
    RGlyph.circle = DrawCircleInGlyph
    RGlyph.square = DrawSquareInGlyph
    RGlyph.element = DrawElementInGlyph
