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

def expand(glyph, distance, join=1, cap=1, src_layer='background', round=False):
    """Expand a glyph's outlines by a given amount of units.

    """
    # get skeleton stroke
    skeleton = glyph.getLayer(src_layer)
    # set undo
    glyph.prepareUndo("expand strokes")
    # calculate outline shape
    outline = make_outline(skeleton, distance, join, cap)
    # clear glyph
    glyph.clear()
    # copy outline to glyph
    outline.drawPoints(glyph.getPointPen())
    # round point positions to integers
    if round:
        glyph.round()
    # done
    glyph.performUndo()
