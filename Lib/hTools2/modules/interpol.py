# [h] hTools2.modules.interpol

'''A collection of tools for working with interpolation.'''

import hTools2.modules.color
reload(hTools2.modules.color)

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.color import clear_color, clear_colors, named_colors

# functions

def interpolate_glyph(gName, f1, f2, f3, factor, clear=True):
    '''
    Interpolates the glyphs with name ``glyph_name`` from masters ``f1`` and ``f2``, with interpolation factor ``(factor_x, factor_y)``, into the destination font ``f3``.

    The optional parameter ``clear`` controls if existing glyphs in ``f3`` should be overwritten.

    '''
    if f2.has_key(gName):
        if clear:
            g = f3.newGlyph(gName, clear=True)
        else:
            g = f3[gName]
        g.interpolate(factor, f1[gName], f2[gName])
        g.changed()
        f3.changed()
    else:
        print 'glyph %s not contained in font 2' % gName

def interpolate_kerning(f1, f2, f3, factor):
    k1 = f1.kerning
    k2 = f2.kerning
    k3 = f3.kerning
    k3.interpolate(k1, k2, factor, True)
    f3.changed()

def check_compatibility(f1, f2, names=None, report=True):
    '''
    Checks if glyphs in ``f1`` and ``f2`` are compatible for interpolation.

    If ``names=None``, all glyphs in ``f1`` will be checked - otherwise, only the ones in the list ``names``.

    Glyph compatibility is indicated by colors in ``f1``:

    - ``green`` -> glyphs are compatible
    - ``red``   -> glyphs are not compatible
    - ``blue``  -> glyph does not exist in ``f2``

    If ``report=True``, the check results will be printed to the output window.

    '''
    # glyph names
    if names != None:
        gNames = names
    else:
        gNames = f1.keys()
    # colors
    clear_colors(f1)
    green = named_colors['green']
    red   = named_colors['red']
    blue  = named_colors['blue']
    # check glyphs
    if report == True:
        print 'checking compatibility between %s and %s...\n' % (get_full_name(f1), get_full_name(f2))
    for name in gNames:
        if f2.has_key(name):
            clear_color(f2[name])
            # if not compatible
            if not f1[name].isCompatible(f2[name]):
                f2[name].markColor = red
                if report == True:
                    print "\t### %s is not compatible" % name
            # if compatible
            else:
                f2[name].markColor = green
                if report == True:
                    print "\t%s is compatible" % name
        # if glyphs not in f2
        else:
            f1[name].markColor = blue
            if report == True:
                print "\t### %s is not in font 2" % name
    # update fonts
    f2.changed()
    f1.changed()
    if report == True:
        print '\n...done.\n'

def condense_glyphs(f3, f1, f2, f1_stem, f2_stem, factor, glyph_names):
    '''Generate condensed glyphs from a 'Regular' font ``f1`` and a 'Bold' font ``f2``.'''
    scale_x = float(f1_stem) / ( f1_stem + factor * (f2_stem - f1_stem ) )
    for glyph_name in glyph_names:
        if not f3.has_key(glyph_name):
            f3.newGlyph(glyph_name)
        f3[glyph_name].prepareUndo('condensomatic')
        f3[glyph_name].interpolate((factor, 0), f1[glyph_name], f2[glyph_name])
        f3[glyph_name].scaleBy((scale_x, 1))
        f3[glyph_name].leftMargin = (f1[glyph_name].leftMargin + f2[glyph_name].leftMargin) * 0.5 * (1.0 - factor)
        f3[glyph_name].rightMargin = (f1[glyph_name].rightMargin + f2[glyph_name].rightMargin) * 0.5 * (1.0 - factor)
        f3[glyph_name].changed()
        f3[glyph_name].performUndo()
    f3.changed()
