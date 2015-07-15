from hTools2.modules.color import clear_colors

f = CurrentFont()

clear_colors(f)

for g in f:
    if len(g) == 0 and len(g.components) == 0:
        g.mark = 1, 0, 0, 0.3
