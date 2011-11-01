# [h] testing color tools

from hTools2.modules.color import clearColors, randomColor
from hTools2.modules.fileutils import getGlyphs

f = CurrentFont()

clearColors(f)

for gName in getGlyphs(f):
    f[gName].mark = randomColor()
