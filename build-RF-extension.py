# [h] build RoboFont Extension

# imports

import os
import hTools2

from mojo.extensions import ExtensionBundle

# data

extension_file = 'hTools2.roboFontExt'
lib_path = os.path.dirname(os.path.dirname(hTools2.__file__))
extension_path = os.path.join(os.path.dirname(lib_path), extension_file)
html_path = os.path.join(lib_path, "Documentation/build/html")

# create bundle

B = ExtensionBundle()
# meta
B.name = "hTools2"
B.developer = 'Gustavo Ferreira'
B.developerURL = 'http://hipertipo.com/'
B.version = "1.6"
B.mainScript = "add-RF-menu.py"
B.launchAtStartUp = True
# lib
B.requiresVersionMajor = '1'
B.requiresVersionMinor = '5'
B.infoDictionary["repository"] = 'gferreira/hTools2'
# html
B.html = True
# save bundle
B.save(extension_path, libPath=lib_path, resourcesPath=None, pycOnly=False) # htmlPath=html_path, 

