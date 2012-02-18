# draw EParagraph

from hTools.objects import hProject
from hTools.tools.ETools_NodeBoxTools import *
from hTools.tools.SampleTools import DeclarationOfRights

# initialize canvas

_ctx.size(960, 800)
_ctx.background(0)

# draw paragraph

p1 = EParagraph('EB17114A', _ctx)
p1.pWidth = 600
p1.leading = 6
p1.pHeight = 600
p1.tracking = 0
p1.c = _ctx.color(1)
p1.txt = DeclarationOfRights['dutch'][:2200]
p1.draw((30, 10),
        frame=True,
        bound=True,
        box=True,
        baseline=True,
        glyphs=True)
