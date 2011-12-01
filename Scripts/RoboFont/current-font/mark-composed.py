# [h] mark composed glyphs

from hTools2.modules.color import clearColors, randomColor

f = CurrentFont()
clearColors(f)
mark_color = randomColor()
for g in f:
	if len(g.components) > 0:
		g.mark = mark_color
		g.update()
f.update()
