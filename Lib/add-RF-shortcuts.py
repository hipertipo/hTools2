# [h] create shortcuts

'''Create RoboFont keyboard shortcuts for scripts in hTools2.'''

import hTools2.modules.sysutils
reload(hTools2.modules.sysutils)

# imports

import os
import random

from hTools2.modules.sysutils import * # build_shortcuts_dict, set_shortcuts, print_shortcuts

from mojo.UI import setScriptingMenuNamingShortKeyForPath

# shortcuts

scripts_path = os.path.join(os.getcwd(), 'Scripts')
#print scripts_path, os.path.exists(scripts_path)

scripts_shortcuts = [
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

# run

scripts_dict = build_shortcuts_dict(scripts_path, scripts_shortcuts)

for path in scripts_dict.keys():
    name = scripts_dict[path]['preferredName']
    shortkey = scripts_dict[path]['shortKey']
    setScriptingMenuNamingShortKeyForPath(path, name, shortkey)

#set_shortcuts(scripts_dict)
#print_shortcuts(verbose=False)
