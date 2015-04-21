# [h] find open contours

f = CurrentFont()

for glyph_name in f.keys():
    for contour in f[glyph_name]:
        if contour.open:
            f[glyph_name].mark = 1, 0, 0, 0.5
