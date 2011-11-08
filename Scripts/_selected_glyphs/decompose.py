# [h] decompose selected glyphs

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

print 'decomposing selected glyphs...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].prepareUndo('decompose')
    f[gName].decompose()
    f[gName].performUndo()
print '...done.'
