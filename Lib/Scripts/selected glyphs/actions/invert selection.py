# [h] invert selection

f = CurrentFont()

for g in f:
    g.selected = not g.selected
