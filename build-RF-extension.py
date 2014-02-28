# [h] build hTools2 as a RoboFont Extension

import os
import hTools2
from mojo.extensions import ExtensionBundle

extension_file = 'hTools2.roboFontExt'
lib_path = os.path.dirname(os.path.dirname(hTools2.__file__))
base_path = os.path.dirname(lib_path)
extension_path = os.path.join(base_path, extension_file)
html_path = os.path.join(base_path, "Documentation/build/html")

B = ExtensionBundle()
B.name = "hTools2"
B.developer = 'Gustavo Ferreira'
B.developerURL = 'http://hipertipo.com/'
B.version = "1.6"
B.mainScript = "add-RF-menu.py"
B.launchAtStartUp = 1
B.addToMenu = []
B.requiresVersionMajor = '1'
B.requiresVersionMinor = '5'
B.infoDictionary["repository"] = 'gferreira/hTools2'
B.infoDictionary["html"] = 1
B.save(extension_path, libPath=lib_path, htmlPath=html_path, resourcesPath=None, pycOnly=False)
