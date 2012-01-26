# [h] mark composed glyphs

import hTools2.modules.color
reload(hTools2.modules.color)

from hTools2.modules.color import *

f = CurrentFont()

clear_colors(f)
mark_color = random_color()

for g in f:
	if len(g.components) > 0:
		g.mark = mark_color
		g.update()

f.update()
