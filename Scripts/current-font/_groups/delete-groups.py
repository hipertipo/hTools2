# [h] delete groups

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import delete_groups

font = CurrentFont()
delete_groups(font)
