# [h] create shortcuts

'''Create RoboFont keyboard shortcuts for scripts in hTools2.'''

import os
from mojo.UI import setScriptingMenuNamingShortKeyForPath, createModifier

shortcuts = [
    (   '1',    'actions',          u'selected-glyphs/actions/actions.py',            ),
    (   'c',    'paint select',     u'selected-glyphs/color/paint-select.py',         ),
    (   'g',    'gridfit',          u'selected-glyphs/transform/gridfit.py',          ),
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

scripts_folder = os.path.join(os.getcwd(), 'Scripts')

for shortcut in shortcuts:
    short_key, name, script_file = shortcut
    script_path = os.path.join(scripts_folder, script_file)
    modifier = createModifier(command=True, shift=True)
    if os.path.exists(script_path):
        # print 'creating shortcut for', script_path
        setScriptingMenuNamingShortKeyForPath(script_path, name, short_key, modifier)
