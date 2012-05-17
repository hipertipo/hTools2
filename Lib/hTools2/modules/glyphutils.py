# [h] hTools2.modules.glyphutils

'''
hTools2.modules.glyphutils
==========================

Functions
---------

### `center_glyph(glyph)`

Centers the `glyph` in its width, leaving `leftMargin` and `rightMargin` with equal values.

    from hTools2.modules.glyphutils import center_glyph
    f = CurrentFont()
    glyph = f['a']
    print glyph.leftMargin, glyph.rightMargin

    >>> 40 78

    center_glyph(glyph)
    print glyph.leftMargin, glyph.rightMargin

    >>> 59 59

### `round_width(glyph, gridsize)`

Rounds `glyph.width` to a multiple of `gridsize`.

    from hTools2.modules.glyphutils import round_width
    f = CurrentFont()
    glyph = f['a']
    print glyph.width

    >>> 525

    round_width(glyph, 100)
    print glyph.width

    >>> 500.0

### `round_margins(glyph, gridsize, left=True, right=True)`

Rounds `glyph.leftMargin` and `glyph.rightMargin` to multiples of `gridsize`.

Use the optional parameters `left` and `right` to turn individual margins of/off.

    from hTools2.modules.glyphutils import round_margins
    f = CurrentFont()
    glyph = f['a']
    print glyph.leftMargin, glyph.rightMargin

    >>> 58 31

    round_margins(glyph, 10)
    print glyph.leftMargin, glyph.rightMargin

    >>> 50.0 30.0

    round_margins(glyph, 11, left=True, right=False)
    print glyph.leftMargin, glyph.rightMargin

    >>> 55.0 30.0

    round_margins(glyph, 11, left=False, right=True)
    print glyph.leftMargin, glyph.rightMargin

    >>> 55.0 33.0

### `has_suffix(glyph, suffix)`

Checks if the name of `glyph` has the extension `suffix`, and returns `True` or `False`.

    from hTools2.modules.glyphutils import has_suffix
    f = CurrentFont()
    glyph = f['a']
    print has_suffix(glyph, 'alt')

    >>> False

    glyph = f['a.alt']
    print has_suffix(glyph, 'alt')

    >>> True

### `change_suffix(glyph, old_suffix, new_suffix=None)`

Returns a new modified name for `glyph`, using `new_suffix` in place of `old_suffix`. If `new_suffix=None`, the suffix is removed and only the base glyph name is used.

    from hTools2.modules.glyphutils import change_suffix
    f = CurrentFont()
    glyph = f['a.alt']
    print change_suffix(glyph, 'alt', 'ALT')

    >>> a.ALT

    print change_suffix(glyph, 'alt')

    >>> a

### `round_points(glyph, (sizeX, sizeY))`

Rounds the position of all `points` in `glyph` to the gridsize `(sizeX,sizeY)`.

    from hTools2.modules.glyphutils import round_points
    f = CurrentFont()
    glyph = f['c']
    for c in glyph:
        for p in c.points:
            print p.x, p.y

    >>> 386 93
    >>> 335 44
    >>> 255 44
    >>> 184 44
    >>> 124 94
    >>> 124 237
    >>> ...

    round_points(glyph, (100, 200))
    for c in glyph:
        for p in c.points:
            print p.x, p.y

    >>> 400.0 0.0
    >>> 300.0 0.0
    >>> 300.0 0.0
    >>> 200.0 0.0
    >>> 100.0 0.0
    >>> 100.0 200.0
    >>> ...

### `round_bpoints(glyph, (sizeX, sizeY))`

Rounds the position of all `bPoints` in `glyph` to the gridsize `(sizeX,sizeY)`.

    from hTools2.modules.glyphutils import round_bpoints
    f = CurrentFont()
    glyph = f['o']
    for c in glyph:
        for p in c.bPoints:
            print p.anchor

    >>> (386, 237)
    >>> (255, 44)
    >>> (124, 237)
    >>> (256, 419)
    >>> ...

    round_bpoints(glyph, (100, 100))
    for c in glyph:
        for p in c.bPoints:
            print p.anchor

    >>> (400.0, 200.0)
    >>> (300.0, 0.0)
    >>> (100.0, 200.0)
    >>> (300.0, 400.0)
    >>> ...

### `round_anchors(glyph, (sizeX, sizeY))`

Rounds the position of all `anchors` in `glyph` to the gridsize `(sizeX,sizeY)`.

    from hTools2.modules.glyphutils import round_anchors
    f = CurrentFont()
    glyph = f['a']
    for a in glyph.anchors:
        print a.name, a.x, a.y

    >>> top 252 527
    >>> bottom 493 0    

    round_anchors(glyph, (50, 50))
    for a in glyph.anchors:
        print a.name, a.x, a.y

    >>> top 250 550
    >>> bottom 500 0

### `select_points_y(glyph, linePos, above=True)`

Selects all points in `glyph` above/below the `linePos(y)`.

    from hTools2.modules.glyphutils import select_points_y
    f = CurrentFont()
    glyph = f['a']
    print glyph.selection

    >>> []

    select_points_y(glyph, 300, above=True)
    print glyph.selection

    >>> [<Point x:135 y:472>, <Point x:194 y:418>, <Point x:354 y:317>, <Point x:87 y:417>, <Point x:252 y:418>, <Point x:424 y:314>, <Point x:424 y:418>, ...]

### `select_points_x(glyph, linePos, left=True)`

Selects all points in `glyph` to left/right of `linePos(x)`.

    from hTools2.modules.glyphutils import select_points_x
    f = CurrentFont()
    glyph = f['a']
    print glyph.selection

    >>> []

    select_points_x(glyph, 300, left=False)
    print glyph.selection

    >>> [<Point x:424 y:80>, <Point x:357 y:65>, <Point x:357 y:17>, <Point x:424 y:418>, <Point x:351 y:21>, <Point x:364 y:472>, <Point x:458 y:-9>, <Point x:474 y:-9>, <Point x:494 y:-8>, <Point x:424 y:314>, <Point x:371 y:230>, <Point x:371 y:279>, <Point x:433 y:48>, <Point x:318 y:418>, ...]

### `deselect_points(glyph)`

Deselect any selected `point` in `glyph`.

    from hTools2.modules.glyphutils import deselect_points
    f = CurrentFont()
    glyph = f['a']
    deselect_points(glyph)

### `shift_selected_points_y(glyph, delta, anchors=False)`

Shift the selected points in `glyph` vertically by `delta` units. If `anchors=True`, anchors will be shifted as well.

### `shift_selected_points_x(glyph, delta, anchors=False)`

Shift the selected points in `glyph` horizontally by `delta` units. If `anchors=True`, anchors will be shifted as well.

### `clear_glyph_libs(glyph)`

Delete all libs in `glyph`.

    from hTools2.modules.glyphutils import clear_glyph_libs
    f = CurrentFont()
    glyph = f['a']
    print glyph.lib.keys()

    >>> ['com.typemytype.robofont.mark']

    clear_glyph_libs(glyph)
    print glyph.lib.keys()    

    >>> []

'''

from math import floor, ceil

#---------
# margins
#---------

def center_glyph(glyph):
	whitespace = glyph.leftMargin + glyph.rightMargin	
	glyph.leftMargin = whitespace / 2
	glyph.rightMargin = whitespace / 2

def round_width(glyph, gridsize):
	_width = glyph.width / gridsize
	glyph.width = round(_width) * gridsize
	glyph.update()

def round_margins(glyph, gridsize, left=True, right=True):
	if left:
		_left = glyph.leftMargin / gridsize
		glyph.leftMargin = round(_left) * gridsize
		glyph.update()
	if right:
		_right = glyph.rightMargin / gridsize
		glyph.rightMargin = round(_right) * gridsize
		glyph.update()

#-------------
# glyph names
#-------------

def has_suffix(glyph, suffix):
	has_suffix = False
	nameParts = glyph.name.split(".")
	if len(nameParts) is 2:
		if nameParts[1] == suffix:
			has_suffix = True
	return has_suffix

def change_suffix(glyph, old_suffix, new_suffix=None):
	_base_name = glyph.name.split(".")[0]
	_old_suffix = glyph.name.split(".")[1]
	if new_suffix is not None:
		_new_name = "%s.%s" % (_base_name, new_suffix)
	else:
		_new_name = _base_name
	return _new_name

#---------------
# round to grid
#---------------

def round_points(glyph, (sizeX, sizeY)):
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
	for contour in glyph.contours:
		for b_point in contour.bPoints:
			_x = float(b_point.anchor[0])
			_y = float(b_point.anchor[1])
			_x_round = round(_x / sizeX) * sizeX
			_y_round = round(_y / sizeY) * sizeY
			b_point.anchor = (_x_round, _y_round)
	glyph.update()

def round_anchors(glyph, (sizeX, sizeY)):
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

def select_points_y(glyph, linePos, invert=False):
	for c in glyph.contours:
		for p in c.points:
			# select points above the line
			if invert != True: 
				if p.y >= linePos:
					p.selected = True
			# select points below the line
			else:
				if p.y <= linePos:
					p.selected = True
	glyph.update()

def select_points_x(glyph, linePos, invert=False):
	for c in glyph.contours:
		for p in c.points:
			if invert == True: 
				if p.x <= linePos:
					p.selected = True
			else:
				if p.x >= linePos:
					p.selected = True
	glyph.update()

def deselect_points(glyph):
	for c in glyph.contours:
		for p in c.points:
			p.selected = False
	glyph.update()

#--------------
# shift points
#--------------

def shift_selected_points_y(glyph, delta, anchors=False):
	for c in glyph.contours:
		for p in c.points:
			if p.selected is True:
				p.y = p.y + delta
	if anchors is True:
		if len(glyph.anchors) > 0:
			for a in glyph.anchors:
				if mode is 1:
					if a.y >= linePos:
						a.y = a.y + delta
				else:
					if a.y <= linePos:
						a.y = a.y + delta
	glyph.update()

def shift_selected_points_x(glyph, delta, anchors=False):
	for c in glyph.contours:
		for p in c.points:
			if p.selected is True:
				p.x = p.x + delta
	if anchors is True:
		if len(glyph.anchors) > 0:
			for a in glyph.anchors:
				if mode == 1:
					if a.x >= linePos:
						a.x = a.x + delta
				else:
					if a.x <= linePos:
						a.x = a.x + delta
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
