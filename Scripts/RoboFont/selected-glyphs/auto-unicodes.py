# [h] auto unicodes

from hTools2.modules.encoding import autoUnicode

f = CurrentFont()

for gName in f.selection:
    autoUnicode(f[gName])
    print f[gName].unicodes
