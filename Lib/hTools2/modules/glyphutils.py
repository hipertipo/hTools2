# [h] hTools2.modules.glyphutils

def centerGlyph(glyph):
    whitespace = glyph.leftMargin + glyph.rightMargin
    glyph.leftMargin = whitespace / 2
    glyph.rightMargin = whitespace / 2

def alignPointsToGrid(glyph, (sizeX, sizeY)):
	for contour in glyph.contours:
		for point in contour.points:
			_x_round = round(point.x / sizeX)
			_y_round = round(point.y / sizeY)
			point.x = int(_x_round * sizeX)
			point.y = int(_y_round * sizeY)
	glyph.update()	

def alignAnchorsToGrid(glyph, (sizeX, sizeY)):
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
