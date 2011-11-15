# [h] transform all open fonts

from hTools2.modules.glyphutils import decompose

# settings

_decompose = True
_remove_overlap = True

# transform

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
