# [h] write glyphs to masters

import os.path

from hTools2.objects import hProject
from hTools.tools.UFOTools import getGlyphs

def writeGlyphsToMaster(font, gNames):
    from robofab.glifLib import GlyphSet
    from robofab.tools.glyphNameSchemes import glyphNameToShortFileName    
    print 'writing glyphs to masters...'
    for gName in gNames:
        g_name = gName.split('.')[0]
        f_name = gName.split('.')[1] + '.ufo'
        p_name = f_name.split('_')[0]
        i_name = '_'.join(f_name.split('_'))
        print '\twriting %s to %s...' % (g_name, f_name)
        p = hProject(p_name)
        glyphs_path = os.path.join(p.paths['ufos'], i_name, "glyphs")
        gs = GlyphSet(glyphs_path, glyphNameToFileNameFunc=glyphNameToShortFileName)
        gs.writeGlyph(g_name, font[gName], font[gName].drawPoints)
        gs.writeContents()
    print '...done.\n'
        
f = CurrentFont()
glyphs = getGlyphs(f)
writeGlyphsToMaster(f, glyphs)
