# [h] paint and arrange groups

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from hTools2.modules.color import paint_groups
from hTools2.modules.messages import no_font_open

f = CurrentFont()

if f is not None:
    paint_groups(f)

else:
    print no_font_open
