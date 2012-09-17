# [h] create shortcuts for scripts

'''create keyboard shortcuts scripts'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.sysutils
    reload(hTools2.modules.sysutils)

# imports

from hTools2.modules.sysutils import *

# hTools2 scripts

_htools2_path = u'/_code/hTools2/Scripts/'
_htools2_shortcuts = [
    (   'a',    'actions',          u'selected-glyphs/_actions/actions.py',            ),
    (   'c',    'paint select',     u'selected-glyphs/_color/paint-select.py',         ),
    (   'f',    'gridfit',          u'selected-glyphs/_transform/gridfit.py',          ),
    (   'h',    'set width',        u'selected-glyphs/_metrics/set-width.py',          ),
    (   'i',    'interpolate',      u'selected-glyphs/_interpol/interpolate.py',       ),
    (   'k',    'mask',             u'selected-glyphs/_layers/mask.py',                ),
    (   'l',    'set margins',      u'selected-glyphs/_metrics/set-margins.py',        ),
    (   'm',    'move',             u'selected-glyphs/_transform/move.py',             ),
    (   'o',    'copy to mask',     u'selected-glyphs/_layers/copy-to-mask.py',        ),
    (   'p',    'copy paste',       u'selected-glyphs/_actions/copy-paste.py',         ),
    (   'r',    'mirror',           u'selected-glyphs/_transform/mirror.py',           ),
    (   's',    'scale',            u'selected-glyphs/_transform/scale.py',            ),
    (   't',    'shift',            u'selected-glyphs/_transform/shift.py',            ),
    (   'v',    'adjust',           u'current-font/_vmetrics/adjust.py',               ),
    (   'w',    'skew',             u'selected-glyphs/_transform/skew.py',             ),
]

# custom production scripts

_hscripts_path = u'/_code/hScripts/'
_hscripts_shortcuts = [
    (   'b',    'build',            u'_objects/hGlyph/build.py',                ),
    (   'z',    'rasterize',        u'_objects/hGlyph/rasterize.py',            ),
    (   'j',    'spacing',          u'_objects/hFont/spacing.py',               ),
    (   'g',    'generate',         u'_objects/hFont/generate.py',              ),
    (   'u',    'groups',           u'_objects/hFont/groups.py',                ),
    (   'e',    'element',          u'_objects/hFont/element.py',               ),
    (   '7',    'outline fonts',    u'_objects/hProject/hires-fonts.py',        ),
    (   '8',    'gridfonts',        u'_objects/hProject/lores-fonts.py',        ),
    (   '9',    'roboproject',      u'_roboflight/roboproject.py',              ),
]

# run

_htools2_dict = build_shortcuts_dict(_htools2_path, _htools2_shortcuts)
_hscripts_dict = build_shortcuts_dict(_hscripts_path, _hscripts_shortcuts)
_shortcuts_dict = merge_shortcuts_dicts( [ _htools2_dict, _hscripts_dict ] )

set_shortcuts(_shortcuts_dict)
print_shortcuts()

