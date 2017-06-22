# [h] find open contours

from hTools2.modules.color import clear_colors

f = CurrentFont()

for glyph_name in f.keys():
    for contour in f[glyph_name]:
        if contour.open:
            f[glyph_name].mark = 1, 0, 0, 0.5
