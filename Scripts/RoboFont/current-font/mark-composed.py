# [h] mark composed glyphs

'''mark glyphs with components'''

from hTools2.modules.color import clearColors

f = CurrentFont()
clearColors(f)

for g in f:
	if len(g.components) > 0:
		g.mark = (0, .5, 1, 1)
		g.update()

f.update()
