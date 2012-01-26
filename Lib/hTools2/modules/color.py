# [h] hTools2.modules.color

from random import random

from hTools2.modules.sysutils import _ctx
from hTools2.plugins.colorsys import *

named_colors = {    
    'red' : hsv_to_rgb(.0, 1, 1) + (1,),
    'orange' : hsv_to_rgb(.11, 1, 1) + (1,),
    'yellow' : hsv_to_rgb(.15, 1, 1) + (1,),
    'green' : hsv_to_rgb(.35, 1, 1) + (1,),
    'cyan' : hsv_to_rgb(.5, 1, 1) + (1,),
    'blue' : hsv_to_rgb(.7, 1, 1) + (1,),
    'purple' : hsv_to_rgb(.8, 1, 1) + (1,),
    'pink' : hsv_to_rgb(.9, 1, 1) + (1,),
}

def random_color():
    # FontLab
    if _ctx == 'FontLab':
        c = int(255 * random())
    # RoboFont & NoneLab
    else:
        R, G, B = hsv_to_rgb(random(), 1.0, 1.0)
        _alpha = 1.0
        c = (R,     G, B, _alpha)
    return c

def clear_colors(font):
    for gName in font.keys():
        clear_color(font[gName])
    font.update()

def clear_color(glyph):
    # FontLab
    if _ctx == 'FontLab':
        g.mark = 0
    # RoboFont & NoneLab
    else:   
        glyph.mark = (1, 1, 1, 0)
    glyph.update()

def paint_groups(f):
    if len(f.groups) > 0:
        clear_colors(f)
        print 'painting glyph groups...\n'
        count = 0
        _order = []
        if f.lib.has_key('groups_order'):
            groups = f.lib['groups_order']
        else:
            groups = f.groups.keys()
        for group in groups:
            color_step = 1.0 / len(f.groups)
            color = color_step * count
            R, G, B = hls_to_rgb(color, 0.5, 1.0)
            print '\tpainting group %s...' % group
            for glyph_name in f.groups[group]:
                if f.has_key(glyph_name) is not True:
                    f.newGlyph(glyph_name)
                _order.append(glyph_name)
                f[glyph_name].mark = (R, G, B, .5)
                f[glyph_name].update()
            count += 1
        f.glyphOrder = _order
        f.update()
        print
        print '...done.\n'
    else:
        print 'font has no groups.\n'
