# [h] auto unicodes

'''Automatically set unicode values for selected glyphs.'''

# imports

from hTools2.modules.encoding import auto_unicode

# run

f = CurrentFont()

if f is not None:
    # current open glyph window
    g = CurrentGlyph()
    if g is not None:
        print 'setting unicode for glyph %s...' % g.name
        auto_unicode(g)
        print '...done.\n'
    else:
        # selected glyphs in font window
        glyph_names = f.selection
        if len(glyph_names) > 0:
            print 'setting unicode for selected glyphs...\n'
            print '\t',
            for glyph_name in glyph_names:
                print glyph_name,
                auto_unicode(f[glyph_name])
            print
            print '\n...done.\n'
        # no glyph selected
        else:
            print 'please select one or more glyphs first.\n'
# no font open
else:
    print 'please open a font first.\n'
