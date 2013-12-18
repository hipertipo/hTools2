# [h] mark composed glyphs

import hTools2.modules.fontutils
reload(hTools2.modules.fontutils)

from hTools2.modules.fontutils import clear_colors, mark_composed_glyphs

# run

f = CurrentFont()

clear_colors(f)
mark_composed_glyphs(f)
