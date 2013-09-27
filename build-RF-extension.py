# [h] build hTools2 as a RoboFont Extension

# imports

import os
import hTools2

from mojo.extensions import ExtensionBundle

# run!

# get extension path
extension_folder = os.path.dirname(os.path.dirname(os.path.dirname(hTools2.__file__)))
extension_name = 'hTools2.roboFontExt'
extension_path = os.path.join(extension_folder, extension_name)

E = ExtensionBundle(path=extension_path, libName="Lib")

print E.libPath()
print E.bundlePath()

#print E.validationErrors
#print E.validate()
#print E.install()