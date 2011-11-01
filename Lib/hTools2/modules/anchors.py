# tools for working with anchors and accented glyphs

def getAnchorsDict(font, gNames=None):
	anchorsDict = { }
	if gNames == None:
		_gNames = font.keys()
	else:
		_gNames = gNames
	for gName in _gNames:
		g = font[gName]
		if len(g.anchors) > 0:
			anchors = []
			for a in g.anchors:
				anchors.append((a.name, a.position))
			anchorsDict[g.name] = anchors
	return anchorsDict
