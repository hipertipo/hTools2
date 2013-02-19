# [h] create shortcuts

'''Create keyboard shortcuts for hTools2 scripts.'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.sysutils
    reload(hTools2.modules.sysutils)

# imports

import os

from hTools2.modules.sysutils import *

# shortcuts

scripts_path = os.getcwd()
scripts_path = os.path.split(scripts_path)[0]

scripts_shortcuts = [
    (   'a',    'actions',          u'selected-glyphs/_actions/actions.py',            ),
    (   'c',    'paint select',     u'selected-glyphs/_color/paint-select.py',         ),
    (   'f',    'gridfit',          u'selected-glyphs/_transform/gridfit.py',          ),
    (   'h',    'set width',        u'selected-glyphs/_metrics/set-width.py',          ),
    (   'i',    'interpolate',      u'selected-glyphs/_interpol/interpolate.py',       ),
    (   'k',    'mask',             u'selected-glyphs/_layers/mask.py',                ),
    (   'l',    'copy to layer',    u'selected-glyphs/_layers/copy-to-layer.py',       ),
    (   'm',    'move',             u'selected-glyphs/_transform/move.py',             ),
    (   'o',    'copy to mask',     u'selected-glyphs/_layers/copy-to-mask.py',        ),
    (   'p',    'copy paste',       u'selected-glyphs/_actions/copy-paste.py',         ),
    (   'r',    'mirror',           u'selected-glyphs/_transform/mirror.py',           ),
    (   's',    'scale',            u'selected-glyphs/_transform/scale.py',            ),
    (   't',    'shift',            u'selected-glyphs/_transform/shift.py',            ),
    (   'v',    'adjust',           u'current-font/_vmetrics/adjust.py',               ),
    (   'w',    'skew',             u'selected-glyphs/_transform/skew.py',             ),
]

# run

scripts_dict = build_shortcuts_dict(scripts_path, scripts_shortcuts)
set_shortcuts(scripts_dict)
print_shortcuts(verbose=True)
