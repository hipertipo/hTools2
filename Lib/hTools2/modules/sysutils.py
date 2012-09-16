# [h] hTools2.modules.sysutils

def get_context():
    # test for FontLab
    try:
        import FL
        _FL = True
    except:
        _FL = False
    # test for RoboFont
    try:
        import mojo
        _RF = True
    except:
        _RF = False
    # if none is True, return `NoneLab`
    if _FL:
        context = 'FontLab'
    elif _RF:
        context = 'RoboFont'
    else:
        context = 'NoneLab'
    # done
    return context

_ctx = get_context()

#-----------
# shortcuts
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
    #------------------------------------------
    #   shortcuts_dict = {
    #       u'/path/to/script.py': {
    #           'preferredName' : 'my script',
    #           'shortKey' : 'n',
    #       }
    #   }
    #------------------------------------------
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
