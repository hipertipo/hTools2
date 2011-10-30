# [h] genenerate current font

from mojo.roboFont import RFont

from hTools2.objects import hProject, hFont
from hTools2.modules.fileutils import walk, deleteFiles

ufo = CurrentFont()
ufo_path = ufo.path
f = hFont(ufo)

print 'generating otf font for %s %s...' % (f.ufo.info.familyName, f.ufo.info.styleName)
otf_path = f.otf_path(test=True)
print '\removing overlaps %s...' % otf_path
f.ufo.removeOverlap()
print '\tgenerating %s...' % otf_path
f.ufo.generate(otf_path, 'otf', glyphOrder=[])
print '\treverting to saved file %s...' % otf_path
ufo.close()
ufo = OpenFont(ufo_path)
print '...done.\n'
