# [h] set basic font names from file name

import hTools2.modules.fontinfo
reload(hTools2.modules.fontinfo)

from hTools2.modules.fontinfo import set_names

f = CurrentFont()
set_names(f)
f.update()