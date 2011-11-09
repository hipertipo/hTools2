# [h] set width for selected glyphs

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

# from hTools2.modules.glyphutils import centerGlyph

def centerGlyph(glyph):
    whitespace = glyph.leftMargin + glyph.rightMargin
    glyph.leftMargin = whitespace / 2
    glyph.rightMargin = whitespace / 2    

# settings

_width = 1000
_center = True

# run script

f = CurrentFont()
gNames = getGlyphs(f)

print 'setting width for selected glyphs...'
for gName in gNames:
    print '\t%s' % gName
    f[gName].prepareUndo('change glyph width')
    f[gName].width = _width
    f[gName].performUndo()
    if _center:
        f[gName].prepareUndo('center glyph')
        centerGlyph(f[gName])
        f[gName].performUndo()
print '...done.\n'

