# [h] hTools2.modules.glyphutils

from math import floor, ceil

# margins

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

# glyph names

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

# round to grid

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

# shift points

def select_points_y(glyph, linePos, above=True):
	for c in glyph.contours:
		for p in c.points:
			# select points above the line
			if above is True: 
				if p.y >= linePos:
					p.selected = True
			# select points below the line
			else:
				if p.y <= linePos:
					p.selected = True
	glyph.update()

def select_points_x(glyph, linePos, left=True):
	for c in glyph.contours:
		for p in c.points:
			if left is True: 
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

# glyph libs

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
