# [h] hTools2.modules.sysutils

import os

# functions

def clean_pyc(directory, path):
    """Remove all .pyc files recursively in path."""
    for file_name in directory:
        file_path = os.path.join(path, file_name)
        if file_name[-3:] == 'pyc':
            print 'deleting %s' % file_name
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clean_pyc(os.listdir(file_path), file_path)

def in_FontLab():
    try:
        import FL
        in_FL = True
    except:
        in_FL = False
    return in_FL

def in_RoboFont():
    try:
        import mojo
        in_RF = True
    except:
        in_RF = False
    return in_RF

def in_DrawBot():
    try:
        import drawBot
        in_DB = True
    except:
        in_DB = False
    return in_DB

def in_NodeBox():
    try:
        import _ctx
        in_NB = True
    except:
        in_NB = False
    return in_NB

def get_context():
    """Get the current environment in which hTools2 is running."""
    _FL = in_FontLab()
    _RF = in_RoboFont()
    if _FL:
        context = 'FontLab'
    elif _RF:
        context = 'RoboFont'
    else:
        context = 'NoneLab'
    return context

# def load_modules(modules_list, debug=True):
#     for module_name in modules_list:
#         exec 'import %s' % module_name
#         if debug:
#             exec 'reload(%s)' % module_name
#         except:
#             print 'could not import module %s' % module_name

#----------------
# RoboFont tools
#----------------

_ctx = get_context()

if _ctx == 'RoboFont':

    from AppKit import NSApp, NSPanel
    from mojo.extensions import getExtensionDefault, setExtensionDefault
    from mojo.UI import getScriptingMenuNamingShortKey, setScriptingMenuNamingShortKey, createModifier, setScriptingMenuNamingShortKeyForPath

    def clear_shortcuts():
        """Remove all current shorcuts."""
        setScriptingMenuNamingShortKey({})

    def get_shortcuts():
        """Get RoboFont shortcuts as a dictionary."""
        return getScriptingMenuNamingShortKey()

    def print_shortcuts(verbose=False):
        """Print all current shorcuts."""
        _dict = getScriptingMenuNamingShortKey()
        for k in _dict:
            name, key = _dict[k]
            print _dict[k][key], _dict[k][name],
            if verbose: print k, os.path.exists(k),
            print
        print

    def set_shortcuts(shortcuts_dict):
        """Set RoboFont shortcuts from a dictionary."""
        # setScriptingMenuNamingShortKey(shortcuts_dict)
        for path in shortcuts_dict.keys():
            preferredName = shortcuts_dict[path]['preferredName']
            shortKey = shortcuts_dict[path]['shortKey']
            modifier = shortcuts_dict[path]['modifier']
            setScriptingMenuNamingShortKeyForPath(path, preferredName, shortKey, modifier)

    def toggle_panels():
        """Show/hide all floating windows in the current workspace."""
        # get panels
        windows = NSApp.windows()
        panels = [ window for window in windows if isinstance(window, NSPanel) ]
        # get state
        show_panels = getExtensionDefault('com.hipertipo.showHidePanels', fallback=True)
        # hide panels
        if show_panels:
            for panel in panels:
                panel.orderOut_(None)
            setExtensionDefault('com.hipertipo.showHidePanels', False)
        # show panels
        if show_panels is False:
            for panel in panels:
                if str(type(panel)) != '<objective-c class NSColorPanel at 0x7fff750fad60>':
                    panel.orderBack_(None)
            setExtensionDefault('com.hipertipo.showHidePanels', True)

def build_shortcuts_dict(path, shortcuts):
    """Build a shortcuts dictionary with script paths, names and shortcut keys."""
    #   shortcuts_dict = {
    #       u'/path/to/script.py': {
    #           'preferredName' : 'my script',
    #           'shortKey' : 'n',
    #           'modifier' : createModifier(command=True, shift=True),
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
            _shortcuts_dict[_file_path]['modifier'] = createModifier(command=True, shift=True)
        else:
            print '%s does not exist.' % _file_path
    return _shortcuts_dict

def merge_shortcuts_dicts(dicts_list):
    """Merge all shortcut dictionaries in a given list."""
    _super_dict = {}
    for _dict in dicts_list:
        for k in _dict.keys():
            _super_dict[k] = _dict[k]
    return _super_dict

# https://code.activestate.com/recipes/208993-compute-relative-path-from-one-directory-to-anothe/

def path_split(p, rest=[]):
    h, t = os.path.split(p)
    if len(h) < 1:
        return [t] + rest
    if len(t) < 1:
        return [h] + rest
    return path_split(h, [t] + rest)

def common_path(l1, l2, common=[]):
    if len(l1) < 1:
        return (common, l1, l2)
    if len(l2) < 1:
        return (common, l1, l2)
    if l1[0] != l2[0]:
        return (common, l1, l2)
    return common_path(l1[1:], l2[1:], common + [l1[0]])

def rel_path(p1, p2):
    common, l1, l2 = common_path(path_split(p1), path_split(p2))
    p = []
    if len(l1) > 0:
        p = [ '../' * len(l1) ]
    p = p + l2
    return os.path.join( *p )
