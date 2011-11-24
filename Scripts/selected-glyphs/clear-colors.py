# [h] clear glyph colors

from hTools2.modules.color import clearColors

f = CurrentFont()

for gName in f.selection:    
    f[gName].mark = (1, 1, 1, 1)
    f[gName].update()

