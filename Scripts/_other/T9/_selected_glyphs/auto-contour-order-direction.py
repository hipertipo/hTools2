# [h] auto countour order & direction

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

print 'auto setting contour order & direction...'
for gName in gNames:
    print '\t%s' % gName
    # auto contour order
    f[gName].prepareUndo('auto contour order')
    f[gName].autoContourOrder()
    f[gName].performUndo()    
    # correct direction
    f[gName].prepareUndo('correct path directions')
    f[gName].correctDirection()
    f[gName].performUndo()
print '...done.'
