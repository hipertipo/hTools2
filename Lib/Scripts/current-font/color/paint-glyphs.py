# [h] paint glyphs

from hTools2.modules.color import hls_to_rgb

f = CurrentFont()

color_step = 1.0 / len(f)

for i, g in enumerate(f):
    hue = i * color_step
    R, G, B = hls_to_rgb(hue, 0.5, 1.0)
    g.mark = (R, G, B, .5)
    g.update()

f.update()
