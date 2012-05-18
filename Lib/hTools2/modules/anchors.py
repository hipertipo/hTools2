# [h] hTools2.modules.anchors

'''tools to remove, create, move and transfer anchors'''

#------------
# font tools
#------------

def get_anchors(font, glyph_names=None):
    '''Get all anchors in specified glyphs as a dict.'''
	anchors_dict = {}
	if glyph_names == None:
		_glyph_names = font.keys()
	else:
		_glyph_names = glyph_names
	for glyph_name in _glyph_names:
		g = font[glyph_name]
		if len(g.anchors) > 0:
			anchors = []
			for a in g.anchors:
				anchors.append((a.name, a.position))
			anchors_dict[g.name] = anchors
	return anchors_dict

#-------------
# glyph tools
#-------------

def rename_anchor(glyph, old_name, new_name):
    '''Rename anchors with name `old_name` in `glyph` to `new_name`.'''
    has_name = False
    if len(glyph.anchors) > 0:
        for a in glyph.anchors:
            if a.name == old_name:
                has_name = True
                a.name = new_name
                glyph.update()
    return has_name

def transfer_anchors(source_glyph, dest_glyph):
    '''Transfer the existing anchors in `source_glyph` to `dest_glyph`.'''
	has_anchor = False
	if len(source_glyph.anchors) > 0 :
		has_anchor = True
		anchorsDict = {}
		for a in source_glyph.anchors:
			anchorsDict[a.name] = a.position
		dest_glyph.clearAnchors()
		for anchor in anchorsDict:
			dest_glyph.appendAnchor(anchor, anchorsDict[anchor])
			dest_glyph.update()
	return has_anchor

def move_anchors(glyph, anchor_names, (delta_x, delta_y)):
    '''Move all anchors with `anchor_names` in `glyph` by `(x, y)` units.'''
    for anchor in glyph.anchors:
		if anchor.name in anchor_names:
			anchor.move((delta_x, delta_y))
			glyph.update()

