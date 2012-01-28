# [h] delete unmarked glyphs

f = CurrentFont()

print 'deleting unmarked glyphs...\n'

for g in f:
    if g.mark == (1, 1, 1, 1):
        print '\tdeleting %s' % g.name
        f.removeGlyph(g.name)
f.update()

print '\n...done.\n'
