# [h] paint glyph groups

from hTools2.modules.color import hls_to_rgb

_sort_groups = False
_sort_glyphs = False

def paintGroups(font):
    if len(font.groups) > 0:
        groups_order = font.groups.keys()
        #groups_order.sort()
        colorStep = 1.0 / len(groups_order)
        color = 0
        glyphs_order = []
        print 'painting glyph groups...\n'
        for group_name in groups_order:
            glyph_names = font.groups[group_name]
            #glyph_names.sort()
            glyphs_order.extend(glyph_names)
            _R, _G, _B = hls_to_rgb(color, 0.5, 1.0)            
            for gName in glyph_names:
                if font.has_key(gName) != True:
                    font.newGlyph(gName)
                font[gName].mark = (_R, _G, _B, .5)
                font[gName].update()
            color = color + colorStep
            if color > 1:
                color = color - 1
        # set glyph order
        font.glyphOrder = []
        font.glyphOrder = glyphs_order
        print '...done.\n'
        font.update()
    else:
        print 'font has no groups.\n'

f = CurrentFont()
paintGroups(f)

