# [h] delete components

from hTools2.modules.fontutils import get_glyphs

f = CurrentFont()
glyph_names = get_glyphs(f)

if len(glyph_names) > 0:
    print 'deleting components in selected glyphs...',
    for glyph_name in glyph_names:
        g = f[glyph_name]
        if len(g.components) > 0:
            for component in g.components:
                # print '\tdeleting %s in %s...' % (component.baseGlyph, g.name)
                g.removeComponent(component)
        g.update()
    print 'done.\n'
else:
    print 'please select a few glyphs first.\n'