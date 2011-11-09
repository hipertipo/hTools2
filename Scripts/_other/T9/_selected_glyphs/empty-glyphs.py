# [h] clear glyph contents

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

print 'emptying selected glyphs...'
for gName in gNames:
    print '\t%s' % gName
    f.newGlyph(gName, clear=True)
print '...done.'
