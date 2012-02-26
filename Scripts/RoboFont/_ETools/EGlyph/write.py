# [e] write EGlyphs to UFOs

import os

from robofab.glifLib import GlyphSet
from robofab.tools.glyphNameSchemes import glyphNameToShortFileName

from hTools.tools.ETools import EWorld, EFont

f = CurrentFont()
w = EWorld()

print "exporting EGlyphs to UFOs...\n"
for EGlyphName in f.selection:
    EName = EGlyphName.split(".")[-1]
    gName = EGlyphName[:-9]
    try:
        g = f[EGlyphName]
        e = EFont(EName, w) 
        _file = e.ufoPath
        gsPath = os.path.join(os.path.dirname(_file), os.path.basename(_file), "glyphs")
        gs = GlyphSet(gsPath, glyphNameToFileNameFunc=glyphNameToShortFileName)
        print "\texporting %s..." % EGlyphName
        gs.writeGlyph(gName, g, g.drawPoints)
        gs.writeContents()
    except KeyError:
        continue
print "\n...done.\n"
