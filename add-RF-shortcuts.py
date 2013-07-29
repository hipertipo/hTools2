# [h] create shortcuts

'''Create RoboFont keyboard shortcuts for scripts in hTools2.'''

# imports

import os

from hTools2.modules.sysutils import *

# shortcuts

scripts_path = os.path.join(os.getcwd(), 'Scripts')

scripts_shortcuts = [
    (   'd',    'actions',          u'selected-glyphs/actions/actions.py',            ),
    (   'c',    'paint select',     u'selected-glyphs/color/paint-select.py',         ),
    (   'f',    'gridfit',          u'selected-glyphs/transform/gridfit.py',          ),
    (   'h',    'set width',        u'selected-glyphs/metrics/set-width.py',          ),
    (   'i',    'interpolate',      u'selected-glyphs/interpol/interpolate.py',       ),
    (   'k',    'mask',             u'selected-glyphs/layers/mask.py',                ),
    (   'l',    'copy to layer',    u'selected-glyphs/layers/copy-to-layer.py',       ),
    (   'm',    'move',             u'selected-glyphs/transform/move.py',             ),
    (   'o',    'copy to mask',     u'selected-glyphs/layers/copy-to-mask.py',        ),
    (   'p',    'copy paste',       u'selected-glyphs/actions/copy-paste.py',         ),
    (   'r',    'mirror',           u'selected-glyphs/transform/mirror.py',           ),
    (   's',    'scale',            u'selected-glyphs/transform/scale.py',            ),
    (   't',    'shift',            u'selected-glyphs/transform/shift.py',            ),
    (   'v',    'adjust',           u'current-font/vmetrics/adjust.py',               ),
    (   'w',    'skew',             u'selected-glyphs/transform/skew.py',             ),
]

# run

scripts_dict = build_shortcuts_dict(scripts_path, scripts_shortcuts)
set_shortcuts(scripts_dict)
print_shortcuts(verbose=False)
