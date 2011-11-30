# [h] hTools2.modules.glyphutils

#---------------
# side-bearings
#---------------

def centerGlyph(glyph):
	whitespace = glyph.leftMargin + glyph.rightMargin
	glyph.leftMargin = whitespace / 2
	glyph.rightMargin = whitespace / 2

def roundMargins(glyph, gridsize, left=True, right=True):
	if left:
		_left_round = round(glyph.leftMargin / gridsize)
		_left = int(_left_round * gridsize)
		glyph.leftMargin = _left
		glyph.update()
	if right:
		_right_round = round(glyph.rightMargin / gridsize)
		_right = int(_right_round * gridsize)
		glyph.rightMargin = _right
		glyph.update()

#-------------
# glyph names
#-------------

def has_suffix(glyph_name, suffix):
	has_suffix = False
	nameParts = glyph_name.split(".")
	if len(nameParts) == 2:
		if nameParts[1] == suffix:
			has_suffix = True
	return has_suffix

def change_suffix(glyph_name, old_suffix, new_suffix=''):
	_base_name = glyph_name.split(".")[0]
	_old_suffix = glyph_name.split(".")[1]
	if new_suffix != '':
		_new_name = "%s.%s" % (_base_name, new_suffix)
	else:
		_new_name = _base_name
	return _new_name

#---------------
# round to grid
#---------------

def roundPointsToGrid(glyph, (sizeX, sizeY)):
	for contour in glyph.contours:
		for point in contour.points:
			_x_round = round(point.x / sizeX)
			_y_round = round(point.y / sizeY)
			point.x = int(_x_round * sizeX)
			point.y = int(_y_round * sizeY)
	glyph.update()	

def roundAnchorsToGrid(glyph, (sizeX, sizeY)):
	if len(glyph.anchors) > 0:
		for anchor in glyph.anchors:
			_x_round = round(float(anchor.x)/sizeX)
			_y_round = round(float(anchor.y)/sizeY)
			x_new = int(_x_round * sizeX)
			y_new = int(_y_round * sizeY)
			x_delta = x_new - anchor.x
			y_delta = y_new - anchor.y
			anchor.move((x_delta, y_delta))
		glyph.update()
