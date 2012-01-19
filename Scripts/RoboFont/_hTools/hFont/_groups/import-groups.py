# [h] import groups from encoding

import hTools2.objects
reload(hTools2.objects)

from hTools2.objects import hFont

ufo = CurrentFont()
font = hFont(ufo)
font.import_groups_from_encoding()
