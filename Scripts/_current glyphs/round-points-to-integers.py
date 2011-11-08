# [h] round point coordenates to integers

# from hTools2.modules.fileutils import getGlyphs

def getGlyphs(f):
	from robofab.world import CurrentGlyph
	gNames = []
	cg = CurrentGlyph()
	if cg is not None:
		gNames.append(cg.name)
	for g in f:
		if g.selected == True:
			if g.name not in gNames:
				gNames.append(g.name)
	return gNames

f = CurrentFont()
gNames = getGlyphs(f)

print 'rounding point positions...'
for gName in gNames:
    print '\trounding %s' % gName
    f[gName].prepareUndo('round point positions')
    f[gName].round()
    f[gName].performUndo()
print '...done.\n'
