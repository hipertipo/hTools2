# [h] create shortcuts for scripts

'''create keyboard shortcuts scripts'''

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.sysutils
    reload(hTools2.modules.sysutils)

# imports

import os

from mojo.UI import getScriptingMenuNamingShortKey, setScriptingMenuNamingShortKey

from hTools2.modules.sysutils import *

# hTools2 scripts

_htools2_path = u'/_code/hTools2/Scripts/'

_htools2_shortcuts = [

    (   'm',    'move',             u'selected-glyphs/_transform/move.py',             ),
    (   'f',    'gridfit',          u'selected-glyphs/_transform/gridfit.py',          ),
    (   't',    'shift',            u'selected-glyphs/_transform/shift.py',            ),
    (   'w',    'skew',             u'selected-glyphs/_transform/skew.py',             ),
    (   'r',    'mirror',           u'selected-glyphs/_transform/mirror.py',           ),
    (   's',    'scale',            u'selected-glyphs/_transform/scale.py',            ),

    (   'h',    'set width',        u'selected-glyphs/_metrics/set-width.py',          ),
    (   'l',    'set margins',      u'selected-glyphs/_metrics/set-margins.py',        ),

    (   'k',    'mask',             u'selected-glyphs/_layers/mask.py',                ),
    (   'o',    'copy to mask',     u'selected-glyphs/_layers/copy-to-mask.py',        ),

    (   'a',    'actions',          u'selected-glyphs/_actions/actions.py',            ),
    (   'p',    'copy paste',       u'selected-glyphs/_actions/copy-paste.py',         ),
    (   'c',    'paint select',     u'selected-glyphs/_color/paint-select.py',         ),
    (   'i',    'interpolate',      u'selected-glyphs/_interpol/interpolate.py',       ),

    (   'v',    'adjust',           u'current-font/_vmetrics/adjust.py',               ),

]

# custom production scripts

_custom_path = u'/_code/hScripts/_objects/'

_custom_shortcuts = [

    (   'b',    'build',            u'hGlyph/build.py',                ),
    (   'z',    'rasterize',        u'hGlyph/rasterize.py',            ),

    (   'j',    'spacing',          u'hFont/spacing.py',               ),
    (   'g',    'generate',         u'hFont/generate.py',              ),
    (   'u',    'groups',           u'hFont/groups.py',                ),
    (   'e',    'element',          u'hFont/element.py',               ),

    (   '7',    'outline fonts',    u'hProject/hires-fonts.py',        ),
    (   '8',    'gridfonts',        u'hProject/lores-fonts.py',        ),
    (   '9',    'RoboProject',      u'hProject/roboproject.py',        ),

]

# set dict

clear_shortcuts()
create_shortcuts()
# print_shortcuts()
