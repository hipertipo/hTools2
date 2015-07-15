# [h] export RF preferences

import os
from mojo.UI import exportPreferences
from robofab.interface.all.dialogs import GetFolder

file_name = 'prefs'
file_folder = GetFolder()

if file_folder is not None:
    file_path = os.path.join(file_folder, file_name)
    print 'saving preferences to %s...' % file_path
    exportPreferences(file_path)
