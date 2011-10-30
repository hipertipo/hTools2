# [h] import glyphs from instances

'''import glyphs from several UFOs into temporary file'''

import os.path

from mojo.roboFont import RFont, RGlyph

from hTools.objects.hProject import hProject
from hTools.objects.hFont import hFont
from hTools.tools.PathTools import deleteFiles, walk

# tools

def tempFont():
    if CurrentFont() is None:
        t = NewFont()
    else:
        t = CurrentFont()
    return t

# settings

projects = [ 'Magnetica', 'Synthetica' ]
glyphs = [ 'a' ]

t = tempFont()

weights = ( 1, 5, 9 )
widths = ( 3, 5 )

for glyphName in glyphs:
    for pName in projects:        
        p = hProject(pName)
        #for i in p.ufoInstances:
        for weight in weights:
            for width in widths:
                ufo_file = '%s-%s%s.ufo' % (p.name, weight, width)
                ufo_path = os.path.join(p.instancesPath, ufo_file)
                ufo = RFont(ufo_path, showUI=False)
                #f = hFont(ufo, p)
                gName = '%s.%s_%s' % (glyphName, ufo.info.familyName, ufo.info.styleName)
                print gName
                tmpGlyph = t.newGlyph(gName, clear=True)
                ufoGlyph = ufo[glyphName]
                pen = tmpGlyph.getPointPen()
                ufoGlyph.drawPoints(pen)
                tmpGlyph.width = ufoGlyph.width
                tmpGlyph.unicodes = ufoGlyph.unicodes
                tmpGlyph.update()
