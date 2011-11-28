# [h] write glyphs to ufo

import os.path

from hTools.objects.hProject import hProject
from hTools.tools.UFOTools import getGlyphs

#def getGlyphs(font):
#    selected = []
#    for g in font:
#        if g.selected:
#            selected.append(g.name)
#    return selected

def writeGlyphsToUfo(font, gNames):
    from robofab.glifLib import GlyphSet
    from robofab.tools.glyphNameSchemes import glyphNameToShortFileName    
    for gName in gNames:
        g_name = gName.split('.')[0]
        f_name = gName.split('.')[1] + '.ufo'
        p_name = f_name.split('_')[0]
        i_name = '-'.join(f_name.split('_'))
        p = hProject(p_name)
        glyphs_path = os.path.join(p.instancesPath, i_name, "glyphs")
        gs = GlyphSet(glyphs_path, glyphNameToFileNameFunc=glyphNameToShortFileName)
        gs.writeGlyph(g_name, font[gName], font[gName].drawPoints)
        gs.writeContents()
        
f = CurrentFont()
glyphs = getGlyphs(f)
writeGlyphsToUfo(f, glyphs)
