# [h] set font names from path

import hTools2.modules.fontinfo
reload(hTools2.modules.fontinfo)

from hTools2.modules.fontinfo import set_names_from_path

f = CurrentFont()
set_names_from_path(f)
f.update()