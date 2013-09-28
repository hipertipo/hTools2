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

extension_dict = {
    "developer" : 'Gustavo Ferreira',
    "developerURL" : 'http://hipertipo.com/',
    "version" : 1.6,
    "mainScript" : "add-RF-menu.py", 
    "launchAtStartUp" : True,
    "addToMenu" : False,
    # lib
    "libPath" : lib_path,
    "requiresVersionMajor" : '1', 
    "requiresVersionMinor": '5',
	"repository" : 'gferreira/hTools2',
    # html
    "html" : True,
    "htmlName" : "html",
    "indexHTMLName": "index.html",
    "htmlPath" : html_path,
}

# create bundle

B = ExtensionBundle('hTools2', path=extension_path)
for key, value in extension_dict.items():
    B.set(key, value)

# save bundle
B.save(extension_path, libPath=lib_path, pycOnly=False)
