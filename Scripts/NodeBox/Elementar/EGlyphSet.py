# [e] draw glyph set

colors = ximport("colors")

from hTools.objects.hProject import hProject
from hTools.tools.ETools_NodeBoxTools import ELine

# script

_ctx.size(1200, 800)
_ctx.background(0)

EName = 'EB09213A'

x = 20
y = 30

p = hProject('Elementar')
groups = p.groupsFromEncoding
for groupName in p.groupsOrder:
    if groupName not in ['invisible','bug']:
        L = ELine(EName, context=_ctx)
        L.gNames = groups[groupName]
        # group name
        _ctx.fill(.7)
        font('Verdana', 11)
        text(groupName, x, y)
        # glyphs
        _ctx.fill(1)
        L.draw((x + 220, y))
        y += int(L.height) + 5
