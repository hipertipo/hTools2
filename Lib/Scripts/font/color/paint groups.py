# [h] paint and arrange groups

from hTools2.modules.encoding import paint_groups
from hTools2.modules.messages import no_font_open

f = CurrentFont()

if f is not None:
    paint_groups(f)

else:
    print no_font_open
