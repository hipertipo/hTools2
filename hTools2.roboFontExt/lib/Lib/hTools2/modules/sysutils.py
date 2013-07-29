# [h] hTools2.modules.sysutils

import os

# functions

def clean_pyc(directory, path):
    '''Remove .pyc files recursively in path.'''
    for file_name in directory:
        file_path = os.path.join(path, file_name)
        if file_name[-3:] == 'pyc':
            print 'deleting %s' % file_name
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clean_pyc(os.listdir(file_path), file_path)

def get_context():
    '''Get the current environment in which hTools2 is running.'''
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
    # if none is `True`, return `NoneLab`
    if _FL:
        context = 'FontLab'
    elif _RF:
        context = 'RoboFont'
    else:
        context = 'NoneLab'
    # done
    return context

# def load_modules(modules_list, debug=True):
#     for module_name in modules_list:
#         exec 'import %s' % module_name
#         if debug:
#             exec 'reload(%s)' % module_name
#         except:
#             print 'could not import module %s' % module_name

# RoboFont shortcut tools

_ctx = get_context()

if _ctx == 'RoboFont':

    from mojo.UI import getScriptingMenuNamingShortKey, setScriptingMenuNamingShortKey

    def clear_shortcuts():
        '''Remove all current shorcuts.'''
        setScriptingMenuNamingShortKey({})

    def get_shortcuts():
        '''Get RoboFont shortcuts as a dictionary.'''
        return getScriptingMenuNamingShortKey()

    def print_shortcuts(verbose=False):
        '''Print all current shorcuts.'''
        _dict = getScriptingMenuNamingShortKey()
        for k in _dict:
            name, key = _dict[k]
            print _dict[k][key], _dict[k][name],
            if verbose: print k, os.path.exists(k),
            print
        print

    def set_shortcuts(shortcuts_dict):
        '''Set RoboFont shortcuts from a dictionary.'''
        setScriptingMenuNamingShortKey(shortcuts_dict)

def build_shortcuts_dict(path, shortcuts):
    '''Build a shortcuts dictionary with script paths, names and shortcut keys.'''
    #   shortcuts_dict = {
    #       u'/path/to/script.py': {
    #           'preferredName' : 'my script',
    #           'shortKey' : 'n',
    #       }
    #   }
    _shortcuts_dict = {}
    for shortcut in shortcuts:
        _key, _name, _file = shortcut
        _file_path = os.path.join(path, _file)
        if os.path.exists(_file_path):
            _shortcuts_dict[_file_path] = {}
            _shortcuts_dict[_file_path]['preferredName'] = _name
            _shortcuts_dict[_file_path]['shortKey'] = _key
        else:
            print '%s does not exist.' % _file_path
    return _shortcuts_dict

def merge_shortcuts_dicts(dicts_list):
    '''Merge all shortcut dictionaries in a given list.'''
    _super_dict = {}
    for _dict in dicts_list:
        for k in _dict.keys():
            _super_dict[k] = _dict[k]
    return _super_dict

