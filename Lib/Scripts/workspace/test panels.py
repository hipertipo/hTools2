# [h] test modules

module_names = [
    'all_fonts',
    'folder',
    'font',
    'glyph',
    'glyphs',
    # 'misc'
]

for module_name in module_names:
    module_path = 'hTools2.dialogs.%s' % module_name
    exec 'import %s as module' % module_path
    for dialog_name in module.__all__:
        command = 'module.%s()' % dialog_name
        exec command
