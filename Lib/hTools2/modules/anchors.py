# [h] hTools2.modules.anchors

# font-level tools

def get_anchors(font, glyph_names=None):
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

# glyph-level tools

def rename_anchor(glyph, old_name, new_name):
    has_name = False
    if len(glyph.anchors) > 0:
        for a in glyph.anchors:
            if a.name == old_name:
                has_name = True
                a.name = new_name
                glyph.update()
    return has_name

def transfer_anchors(source_glyph, dest_glyph):
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
