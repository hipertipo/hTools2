# [h] clear font guides

from mojo.roboFont import CurrentFont
from hTools2.modules.fontutils import clear_guides
from hTools2.modules.messages import no_font_open

f = CurrentFont()

if f is not None:
    clear_guides(f)

else:
    print no_font_open
