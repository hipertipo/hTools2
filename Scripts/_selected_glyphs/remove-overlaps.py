# [h] remove overlaps

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

print 'removing overlaps...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].prepareUndo('remove overlaps')
    f[gName].removeOverlap()
    f[gName].performUndo()
print '...done.\n'
