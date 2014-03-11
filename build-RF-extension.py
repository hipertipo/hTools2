# [h] build hTools2 as a RoboFont Extension

import os
from mojo.extensions import ExtensionBundle

extension_file = 'hTools2.roboFontExt'
base_path = os.path.dirname(__file__)
lib_path = os.path.join(base_path, 'Lib')
extension_path = os.path.join(base_path, extension_file)
html_path = os.path.join(base_path, "Documentation/build/html")
os.makedirs(html_path)

print 'building extension...',

B = ExtensionBundle()
B.name = "hTools2"
B.developer = 'Gustavo Ferreira'
B.developerURL = 'http://hipertipo.com/'
B.version = "1.6"
B.mainScript = "init-RF-extension.py"
B.launchAtStartUp = 1
B.addToMenu = []
B.requiresVersionMajor = '1'
B.requiresVersionMinor = '5'
B.infoDictionary["repository"] = 'gferreira/hTools2'
B.infoDictionary["html"] = 1
B.save(extension_path, libPath=lib_path, htmlPath=html_path, resourcesPath=None, pycOnly=False)

print 'done.'