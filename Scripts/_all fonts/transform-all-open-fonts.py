# [h] transform all open fonts

_decompose = True
_remove_overlap = True

def decompose(f):
	for g in f:
		g.decompose()
		g.update()
	f.update()	

print 'transforming all open fonts...\n'
for font in AllFonts():
    print '\tdecomposing %s %s...' % (font.info.familyName, font.info.styleName)
    decompose(font)
    print '\tremoving overlaps from %s %s...' % (font.info.familyName, font.info.styleName)
    font.removeOverlap()
    print
print '...done.\n'
