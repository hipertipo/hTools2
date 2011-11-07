# [h] genenerate current font

from mojo.roboFont import RFont

from hTools2.objects import hProject, hFont

ufo = CurrentFont()
f = hFont(ufo)

print 'generating otf font for %s %s...' % (f.ufo.info.familyName, f.ufo.info.styleName)
otf_path = f.otf_path()
print '\tremoving overlaps...'
f.ufo.removeOverlap()
print '\tgenerating as %s...' % otf_path
f.ufo.generate(otf_path, 'otf', glyphOrder=[])
print '\treverting to saved file...'
f.ufo.close()
ufo = OpenFont(f.ufo.path)
print '...done.\n'

#print f.ufo.features
#print f.ufo.lib.keys()
