# [h] hTools2.modules.outline

"""A simple wrapper for Frederik Berlaen's outliner code."""

# imports

from hTools2.extras.outline import *

from mojo.roboFont import NewFont

# functions

def make_outline(glyph, distance, join, cap):
    """
    Calculate expanded outlines for a given glyph.

    """
    options = ['Square', 'Round', 'Butt']
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

def expand_glyph(src_glyph, dst_glyph, distance, join=1, cap=1, round=False):
    """
    Expand a glyph's outlines by a given amount of units.

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

expand = expand_glyph

def expand_font(src_font, distance, join=1, cap=1):
    # create a new empty font
    dst_font = NewFont(showUI=False)
    # expand all glyph
    for glyph_name in src_font.keys():
        # get source glyph
        src_glyph = src_font[glyph_name]
        # get dest glyph
        dst_font.newGlyph(glyph_name)
        dst_glyph = dst_font[glyph_name]
        # expand glyph into dest font
        outline_pen = make_outline(src_glyph, distance, join, cap)
        outline_pen.drawPoints(dst_glyph.getPointPen())
        # copy width from source glyph
        dst_glyph.width = src_glyph.width
        # copy components
        if len(src_glyph.components):
            for component in src_glyph.components:
                dst_glyph.appendComponent(component.baseGlyph, component.offset, component.scale)
    # done
    return dst_font
