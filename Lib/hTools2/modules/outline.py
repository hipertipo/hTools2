# [h] hTools2.modules.outline

"""A simple wrapper for Frederik Berlaen's outliner code."""

# imports

from hTools2.extras.outline import *

# functions

def make_outline(glyph, distance, join, cap):
    """Calculate expanded outlines for a given glyph.

    """
    options = [ 'Square', 'Round', 'Butt' ]
    pen = OutlinePen(glyph.getParent(),
        distance,
        connection=options[join],
        cap=options[cap],
        miterLimit=None,
        closeOpenPaths=True)
    glyph.draw(pen)
    pen.drawSettings(drawOriginal=False,
        drawInner=True,
        drawOuter=True)
    return pen

def expand(src_glyph, dst_glyph, distance, join=1, cap=1, round=False):
    """Expand a glyph's outlines by a given amount of units.

    """
    # set undo
    dst_glyph.prepareUndo("expand strokes")
    # calculate outline shape
    outline_pen = make_outline(src_glyph, distance, join, cap)
    # clear glyph
    dst_glyph.clear()
    # copy outline to glyph
    outline_pen.drawPoints(dst_glyph.getPointPen())
    # round point positions to integers
    if round:
        dst_glyph.round()
    # done
    dst_glyph.performUndo()
