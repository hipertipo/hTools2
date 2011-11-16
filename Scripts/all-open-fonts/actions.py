# [h] perform actions on all open fonts

# from hTools2.modules.fontutils import decompose, autoContourOrderDirection

def decompose(font):
	for g in font:
		g.decompose()
		
# settings

_decompose = True
_remove_overlap = True

# run

print 'transforming all open fonts...\n'
for font in AllFonts():
    # decompose
    print '\tdecomposing %s %s...' % (font.info.familyName, font.info.styleName)
    decompose(font)
    # remove overlap
    print '\tremoving overlaps from %s %s...' % (font.info.familyName, font.info.styleName)
    font.removeOverlap()
    print
print '...done.\n'
