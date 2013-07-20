import os
from mojo.extensions import *

code_path = os.getcwd()
B = ExtensionBundle(path=code_path, libName="Lib")
B.name = 'hTools2'
B.version = '1.0'
B.developer = 'Gustavo Ferreira'
B.developerURL = 'http://hipertipo.com/'
B.launchAtStartUp = True
B.addToMenu = False

print dir(B)
print B.infoDictionary
#print B.fileName()
#print B.infoDictionaryPath()
#print B.libPath()
#print B.bundleExists()
#print B.validateLib()
#print B.validateInfo()
#print B.validationErrors()
#B.install()
B.get()