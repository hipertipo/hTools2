# [h] clear unicodes

'''Clear unicode values from selected glyphs.'''

f = CurrentFont()

for gName in f.selection:
    f[gName].unicodes = []
