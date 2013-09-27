# [h] create anchors

'''Create `top` and `bottom` anchors in selected glyphs.'''

# import

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.anchors import create_anchors

# settings

_top = True
_bottom = True
_accent = False
_top_delta = 20
_bottom_delta = 20

# run

f = CurrentFont()

print 'creating anchors in glyphs...\n'
print '\t',
for glyph_name in get_glyphs(f):
    print glyph_name,
    f[glyph_name].prepareUndo('create anchors')
    create_anchors(f[glyph_name], top=_top, bottom=_bottom, accent=_accent, top_delta=_top_delta, bottom_delta=_bottom_delta)
    f[glyph_name].performUndo()
f.update()
print
print "\n...done.\n"

