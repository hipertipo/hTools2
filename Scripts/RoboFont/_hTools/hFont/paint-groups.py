# [h] paint groups

import hTools2.objects
reload(hTools2.objects)

from hTools2.objects import hProject, hFont

ufo = CurrentFont()
font = hFont(ufo)
font.order_glyphs()
font.paint_groups()
