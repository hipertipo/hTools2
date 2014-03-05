# [h] remove duplicate anchors

from mojo.roboFont import CurrentFont

from hTools2.modules.anchors import remove_duplicate_anchors
from hTools2.modules.messages import no_font_open

f = CurrentFont()

if f is not None:
    remove_duplicate_anchors(f)

else:
    print no_font_open
