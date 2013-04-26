# [h] drawing primitives

# magic constant for drawing circular arcs with beziers (thanks EvB)
BEZIER_ARC_MAGIC = 0.5522847498

def rect(pen, x, y, size):
    pen.moveTo( (x, y) )
    pen.lineTo( (x, y + size) )
    pen.lineTo( (x + size, y + size) )
    pen.lineTo( (x + size, y) )
    pen.closePath()

def ellipse( pen, (x, y, rx, ry) ):
    bcpx = BEZIER_ARC_MAGIC * rx
    bcpy = BEZIER_ARC_MAGIC * ry
    pen.moveTo( (x, y + rx) )
    pen.curveTo( (x + bcpx, y + ry), (x + rx, y + bcpy), (x + rx, y) )
    pen.curveTo( (x + rx, y - bcpy), (x + bcpx, y - ry), (x, y - ry) )
    pen.curveTo( (x - bcpx, y - ry), (x - rx, y - bcpy), (x - rx, y) )
    pen.curveTo( (x - rx, y + bcpy), (x - bcpx, y + ry), (x, y + ry) )
    pen.closePath()

def oval(pen, x, y, size):
    radius = (size / 2)
    bcp = BEZIER_ARC_MAGIC * radius
    x += radius
    y += radius
    pen.moveTo((x, y+radius))
    pen.curveTo((x+bcp, y+radius), (x+radius, y+bcp), (x+radius, y) )
    pen.curveTo((x+radius, y-bcp), (x+bcp, y-radius), (x, y-radius) )
    pen.curveTo((x-bcp, y-radius), (x-radius, y-bcp), (x-radius, y) )
    pen.curveTo((x-radius, y+bcp), (x-bcp, y+radius), (x, y+radius) )
    pen.closePath()

def element(pen, x, y, size, magic=BEZIER_ARC_MAGIC):
    bcp = magic * (size / 2)
    x = x + (size / 2)
    y = y + (size / 2)
    pen.moveTo( (x, y + (size / 2)) )
    pen.curveTo( (x + bcp, y + (size / 2)), (x + (size / 2), y + bcp), (x + (size / 2), y) )
    pen.curveTo( (x + (size / 2), y - bcp), (x + bcp, y - (size / 2)), (x, y - (size / 2)) )
    pen.curveTo( (x - bcp, y - (size / 2)), (x - (size / 2), y - bcp), (x - (size / 2), y) )
    pen.curveTo( (x - (size / 2), y + bcp), (x - bcp, y + (size / 2)), (x, y + (size / 2)) )
    pen.closePath()
