# [h] create shortcuts for scripts

'''create keyboard shortcuts scripts'''

import os

from mojo.UI import getScriptingMenuNamingShortKey, setScriptingMenuNamingShortKey

#-----------
# functions
#-----------

def clear_shortcuts():
    setScriptingMenuNamingShortKey({})

def print_shortcuts():
    _dict = getScriptingMenuNamingShortKey()
    for k in _dict:
        name, key = _dict[k]
        print _dict[k][key], _dict[k][name], k, os.path.exists(k)

def set_shortcuts(shortcuts_dict):
    setScriptingMenuNamingShortKey(shortcuts_dict)

def build_shortcuts_dict(path, shortcuts):
    #   shortcuts_dict = {  
    #       u'/path/to/script.py': {
    #           'preferredName' : 'my script',
    #           'shortKey' : 'n',
    #       }
    #   }  
    _shortcuts_dict = {}
    for shortcut in shortcuts:
        _key, _name, _file = shortcut
        _file_path = path + _file
        if os.path.exists(_file_path):
            _shortcuts_dict[_file_path] = {}
            _shortcuts_dict[_file_path]['preferredName'] = _name
            _shortcuts_dict[_file_path]['shortKey'] = _key
        else:
            print '%s does not exist.' % _file_path
    return _shortcuts_dict

def merge_shortcuts_dicts(dicts_list):
    _super_dict = {}
    for _dict in dicts_list:
        for k in _dict.keys():
            _super_dict[k] = _dict[k]
    return _super_dict

def create_shortcuts():
    htools2_dict = build_shortcuts_dict(_htools2_path, _htools2_shortcuts)
    custom_dict = build_shortcuts_dict(_custom_path, _custom_shortcuts)
    shortcuts_dict = merge_shortcuts_dicts( [ htools2_dict, custom_dict ] )
    set_shortcuts(shortcuts_dict)

#--------------
# scripts data
#--------------

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

_custom_path = u'/_code/hScripts/'

_custom_shortcuts = [

    (   'b',    'build',            u'hGlyph/build.py',                ),
    (   'z',    'rasterize',        u'hGlyph/rasterize.py',            ),

    (   'j',    'spacing',          u'hFont/spacing.py',               ),
    (   'g',    'generate',         u'hFont/generate.py',              ),
    (   'u',    'groups',           u'hFont/groups.py',                ),
    (   'e',    'element',          u'hFont/element.py',               ),

    (   '7',    'outline fonts',    u'hProject/hires-fonts.py',        ),
    (   '8',    'gridfonts',        u'hProject/lores-fonts.py',        ),

]

#----------
# set dict
#----------

# clear_shortcuts()
create_shortcuts()
# print_shortcuts()
