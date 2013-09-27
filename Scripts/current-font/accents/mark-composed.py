# [h] mark composed glyphs

'''Mark all composed glyphs in font.'''

# import

from hTools2.modules.color import clear_colors, random_color

# run

f = CurrentFont()

clear_colors(f)
mark_color = random_color()

for g in f:
    if len(g.components) > 0:
        g.mark = mark_color
        g.update()

f.update()
