# [h] clear anchors

'''Delete all anchors in the selected glyphs.'''

# import

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import get_glyphs

# run

f = CurrentFont()

print 'deleting anchors in glyphs...\n'
print '\t',
for glyph_name in get_glyphs(f):
    if len(f[glyph_name].anchors) > 0:
        print glyph_name,
        f[glyph_name].prepareUndo('clear anchors')
        f[glyph_name].clearAnchors()
        f[glyph_name].update()
        f[glyph_name].performUndo()
f.update()
print
print "\n...done.\n"
