# [h] hTools2.modules.glyphutils

"""A collection of functions for working with glyphs."""

from math import floor, ceil

#---------
# margins
#---------

def center_glyph(glyph):
    """Center the ``glyph`` in its advance width, leaving ``leftMargin`` and ``rightMargin`` with equal values."""
    whitespace = glyph.leftMargin + glyph.rightMargin
    glyph.leftMargin = whitespace / 2
    glyph.rightMargin = whitespace / 2

def round_width(glyph, gridsize):
    """Round ``glyph.width`` to a multiple of ``gridsize``."""
    _width = float(glyph.width) / gridsize
    glyph.width = round(_width) * gridsize
    glyph.update()

def round_margins(glyph, gridsize, left=True, right=True):
    """Round left and/or right margins to multiples of ``gridsize``."""
    if left:
        _left = float(glyph.leftMargin) / gridsize
        glyph.leftMargin = round(_left) * gridsize
        glyph.update()
    if right:
        _right = float(glyph.rightMargin) / gridsize
        glyph.rightMargin = round(_right) * gridsize
        glyph.update()

#-------------
# glyph names
#-------------

def has_suffix(glyph, suffix):
    """Check if the name of ``glyph`` has the extension ``suffix``, and returns ``True`` or ``False``."""
    has_suffix = False
    nameParts = glyph.name.split(".")
    # check for suffix
    if len(nameParts) == 2:
        if nameParts[1] == suffix:
            has_suffix = True
    # check for no suffix
    else:
        if len(nameParts) == 1 and len(suffix) == 0:
            has_suffix = True
    return has_suffix

def change_suffix(glyph, old_suffix, new_suffix=None):
    """Return a new modified name for ``glyph``, using ``new_suffix`` in place of ``old_suffix``."""
    base_name = glyph.name.split(".")[0]
    if new_suffix is not None:
        new_name = "%s.%s" % (base_name, new_suffix)
    else:
        new_name = base_name
    return new_name

#---------------
# round to grid
#---------------

def round_points(glyph, (sizeX, sizeY)):
    """Round the position of all ``points`` in ``glyph`` to the gridsize ``(sizeX,sizeY)``."""
    for contour in glyph.contours:
        for point in contour.points:
            _x = float(point.x)
            _y = float(point.y)
            _x_round = round(_x / sizeX) * sizeX
            _y_round = round(_y / sizeY) * sizeY
            point.x = _x_round
            point.y = _y_round
    glyph.update()

def round_bpoints(glyph, (sizeX, sizeY)):
    """Round the position of all ``bPoints`` in ``glyph`` to the gridsize ``(sizeX,sizeY)``."""
    for contour in glyph.contours:
        for b_point in contour.bPoints:
            _x = float(b_point.anchor[0])
            _y = float(b_point.anchor[1])
            _x_round = round(_x / sizeX) * sizeX
            _y_round = round(_y / sizeY) * sizeY
            b_point.anchor = (_x_round, _y_round)
    glyph.update()

def round_anchors(glyph, (sizeX, sizeY)):
    """Round the position of all ``anchors`` in ``glyph`` to the gridsize ``(sizeX,sizeY)``."""
    if len(glyph.anchors) > 0:
        for anchor in glyph.anchors:
            _x_round = round(float(anchor.x) / sizeX)
            _y_round = round(float(anchor.y) / sizeY)
            x_new = int(_x_round * sizeX)
            y_new = int(_y_round * sizeY)
            x_delta = x_new - anchor.x
            y_delta = y_new - anchor.y
            anchor.move((x_delta, y_delta))
        glyph.update()

#---------------
# select points
#---------------

def select_points_x(glyph, linePos, side='left'):
    """Select all points in ``glyph`` to left/right of ``linePos(x)``."""
    for c in glyph.contours:
        for p in c.points:
            # select points to the left of the line
            if side == 'left':
                if p.x <= linePos:
                    p.selected = True
            # select points to the right of the line
            else:
                if p.x >= linePos:
                    p.selected = True
    glyph.update()

def select_points_y(glyph, linePos, side='top'):
    """Select all points in ``glyph`` above/below the ``linePos(y)``."""
    for c in glyph.contours:
        for p in c.points:
            # select points above the line
            if side == 'top':
                if p.y >= linePos:
                    p.selected = True
            # select points below the line
            else:
                if p.y <= linePos:
                    p.selected = True
    glyph.update()

def deselect_points(glyph):
    """Deselect any selected ``point`` in ``glyph``."""
    for c in glyph.contours:
        for p in c.points:
            p.selected = False
    glyph.update()

#--------------
# shift points
#--------------

def shift_selected_points_x(glyph, delta, anchors=False, bPoints=True):
    """Shift the selected points in ``glyph`` horizontally by ``delta`` units."""
    # shift bPoints
    if bPoints:
        for c in glyph.contours:
            for p in c.bPoints:
                if p.selected:
                    # shift anchor point
                    px, py = p.anchor
                    px += delta
                    p.anchor = px, py
                    # shift handles
                    bcpIn_x, bcpIn_y = p.bcpIn
                    bcpOut_x, bcpOut_y = p.bcpOut
                    bcpIn_x += delta
                    bcpOut_x += delta
                    p.bcpIn = bcpIn_x, bcpIn_y
                    p.bcpOut = bcpOut_x, bcpOut_y
    # shift points
    else:
        for c in glyph.contours:
            for p in c.points:
                if p.selected is True:
                    p.x = p.x + delta
    # shift anchors
    if anchors:
        if len(glyph.anchors) > 0:
            for a in glyph.anchors:
                if mode == 1:
                    if a.x >= linePos:
                        a.x = a.x + delta
                else:
                    if a.x <= linePos:
                        a.x = a.x + delta
    # done
    glyph.update()

def shift_selected_points_y(glyph, delta, anchors=False, bPoints=True):
    """Shift the selected points in ``glyph`` vertically by ``delta`` units."""
    # shift bPoints
    if bPoints:
        for c in glyph.contours:
            for p in c.bPoints:
                if p.selected:
                    # shift anchor point
                    px, py = p.anchor
                    py += delta
                    p.anchor = px, py
                    # shift handles
                    bcpIn_x, bcpIn_y = p.bcpIn
                    bcpOut_x, bcpOut_y = p.bcpOut
                    bcpIn_y += delta
                    bcpOut_y += delta
                    p.bcpIn = bcpIn_x, bcpIn_y
                    p.bcpOut = bcpOut_x, bcpOut_y
    # shift points
    else:
        for c in glyph.contours:
            for p in c.points:
                if p.selected:
                    p.y = p.y + delta
    # shift anchors
    if anchors:
        if len(glyph.anchors) > 0:
            for a in glyph.anchors:
                if mode is 1:
                    if a.y >= linePos:
                        a.y = a.y + delta
                else:
                    if a.y <= linePos:
                        a.y = a.y + delta
    # done
    glyph.update()

#---------------
# center glyphs
#---------------

def draw_bounds(g, (x1, y1, x2, y2), (x3, y3)):
    # x guides
    g.addGuide((x1, 0), 90, name="x_min")
    g.addGuide((x2, 0), 90, name="x_max")
    g.addGuide((x3, 0), 90, name="x_mid")
    # y guides
    g.addGuide((0, y1), 0, name="y_min")
    g.addGuide((0, y2), 0, name="y_max")
    g.addGuide((0, y3), 0, name="y_mid")
    # done
    g.update()

def get_bounds(g, layer_names):
    lowest_x = False
    lowest_y = False
    highest_x = False
    highest_y = False
    for layer_name in layer_names:
        glyph = g.getLayer(layer_name)
        if glyph.box is not None:
            xMin, yMin, xMax, yMax = glyph.box
            # lowest x
            if not lowest_x:
                lowest_x = xMin
            else:
                if xMin < lowest_x:
                   lowest_x = xMin
            # lowest y
            if not lowest_y:
                lowest_y = yMin
            else:
                if yMin < lowest_y:
                   lowest_y = yMin
            # highest x
            if not highest_x:
                highest_x = xMax
            else:
                if xMax > highest_x:
                    highest_x = xMax
            # highest y
            if not highest_y:
                highest_y = yMax
            else:
                if yMax > highest_y:
                    highest_y = yMax
    # done
    return (lowest_x, lowest_y, highest_x, highest_y)

def get_middle((lo_x, lo_y, hi_x, hi_y)):
    width_all = hi_x - lo_x
    height_all = hi_y - lo_y
    middle_x = lo_x + (width_all * .5)
    middle_y = lo_x + (height_all * .5)
    return (middle_x, middle_y)

def center_layers(g, layer_names, (middle_x, middle_y)):
    for layer_name in layer_names:
        glyph = g.getLayer(layer_name)
        if glyph.box is not None:
            xMin, yMin, xMax, yMax = glyph.box
            w = xMax - xMin
            h = yMax - yMin
            center_x = xMin + (w * .5)
            center_y = yMin + (h * .5)
            shift_x = middle_x - center_x
            shift_y = middle_y - center_y
            glyph.move((shift_x, shift_y))
        g.update()

def center_glyph_layers(g, layers, guides=True):
    _bounds = get_bounds(g, layers)
    _middle = get_middle(_bounds)
    center_layers(g, layers, _middle)
    if guides:
        clear_guides(g)
        _bounds = get_bounds(g, layers)
        _middle = get_middle(_bounds)
        draw_bounds(g, _bounds, _middle)

#------------
# glyph libs
#------------

def check_lib(glyph):
    if len(glyph.lib.keys()) > 0:
        return True
        print 'glyph libs:', g.lib.keys()
    else:
        print "glyph doesn't have any libs.\n"
        return False

def clear_glyph_libs(glyph):
    """Delete all libs in ``glyph``."""
    if check_lib(glyph) is True:
        for k in glyph.lib.keys():
            del glyph.lib[k]
        glyph.update()

#------------
# guidelines
#------------

def clear_guides(glyph):
    for guide in glyph.guides:
        glyph.removeGuide(guide)
    glyph.update()

#------
# bcps
#------

def equalize_bcps(glyph):
    """Equalize ``bcps`` from selected points in glyph."""
    glyph.prepareUndo()
    for contour in glyph.contours:
        for point in contour.bPoints:
            if point.selected:
                x, y = point.bcpIn
                if x <> 0:
                    point.bcpIn = (x, 0)
                    point.bcpOut = (-x, 0)
                if y <> 0:
                    point.bcpIn = (0, y)
                    point.bcpOut = (0, -y)
    glyph.performUndo()

def retract_bcps(glyph):
    """Retract ``bcps`` from selected points in glyph."""
    glyph.prepareUndo()
    for contour in glyph:
        for point in contour.bPoints:
            if point.selected:
                point.bcpIn = (0, 0)
                point.bcpOut = (0, 0)
    glyph.performUndo()

