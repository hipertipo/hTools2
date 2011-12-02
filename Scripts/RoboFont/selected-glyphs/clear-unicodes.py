# [h] clear unicodes

f = CurrentFont()

for gName in f.selection:
    f[gName].unicodes = []
