# [h] import glyphs from masters

import os.path

from mojo.roboFont import CurrentFont, RFont, RGlyph

from hTools2.objects import hProject, hFont
from hTools2.modules.fileutils import *

def tempFont():
	if CurrentFont() is None:
		t = RFont(showUI=True)
	else:
		t = CurrentFont()
	return t

projects = [ 'Magnetica', 'Quantica', 'Jornalistica'  ]
glyphs = [ 'n', 'o',]

t = tempFont()

print 'importing glyphs...'
for glyphName in glyphs:
	 for pName in projects:
		 p = hProject(pName)
		 for ufo_path in p.masters():
			 ufo = RFont(ufo_path, showUI=False)
			 gName = '%s.%s_%s' % (glyphName, ufo.info.familyName, ufo.info.styleName)
			 print '\timporting %s from %s %s'% (glyphName, ufo.info.familyName, ufo.info.styleName)
			 tmpGlyph = t.newGlyph(gName, clear=True)
			 ufoGlyph = ufo[glyphName]
			 pen = tmpGlyph.getPointPen()
			 ufoGlyph.drawPoints(pen)
			 tmpGlyph.width = ufoGlyph.width
			 tmpGlyph.unicodes = ufoGlyph.unicodes
			 tmpGlyph.update()
print '...done.\n'

