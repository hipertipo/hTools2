# [h] clear glyph colors

f = CurrentFont()

for gName in f.selection:    
    f[gName].mark = (1, 1, 1, 1)
    f[gName].update()
