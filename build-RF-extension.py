# [h] build hTools2 as a RoboFont Extension

# imports

import os
import shutil
import plistlib
import time

from mojo.extensions import *

import hTools2

# functions

def copy_files(source_path, dest_path):
    """"Copy all files from one folder to another."""
    for root, dirs, files in os.walk(source_path):
        dest = dest_path + root.replace(source_path, '')
        if not os.path.isdir(dest):
            os.mkdir(dest)
        # loop through all files in the directory
        for f in files:
            file_name, extension = os.path.splitext(f)
            # ignore files
            if extension != '.pyc' and f[0] != '.':
                    old_loc = os.path.join(root, f)
                    new_loc = os.path.join(dest, f)
                    # copy file
                    if not os.path.isfile(new_loc):
                        # print 'copying file from %s to %s.' % (old_loc, new_loc)
                        shutil.copy2(old_loc, new_loc)

# parameters

_test = True

# run!

print 'building hTools2 extension...\n'

# get extension path
extension_folder = os.path.dirname(os.path.dirname(os.path.dirname(hTools2.__file__)))
extension_name = 'hTools2.roboFontExt'
extension_path = os.path.join(extension_folder, extension_name)

# create extension package    
print '\tcreating extension package...'
if os.path.exists(extension_path):
    shutil.rmtree(extension_path)
os.makedirs(extension_path)

# create lib folder
print '\tbuilding lib folder...'
libs_path_src = os.path.dirname(os.path.dirname(hTools2.__file__))
libs_path_ext = os.path.join(extension_path, 'lib')
os.makedirs(libs_path_ext)
copy_files(libs_path_src, libs_path_ext)

# create html folder
print '\tbuilding html folder...'
html_path_src = os.path.join(extension_folder, 'Documentation/build/html')
html_path_ext = os.path.join(extension_path, 'html')
os.makedirs(html_path_ext)
copy_files(html_path_src, html_path_ext)

# create info.plist
print '\tcreating info.plist...'
plist_path = os.path.join(extension_path, 'info.plist')
info = {
    'addToMenu' : [],
    'name' : 'hTools2',
    'version' : '1.6',
    'developer' : 'Gustavo Ferreira',
    'developerURL' : 'http://hipertipo.com/',
    'html' : True,
    'launchAtStartUp' : True,
    'mainScript' : 'add-RF-menu.py',
    'timeStamp' : time.time(),
}
plistlib.writePlist(info, plist_path)

print
print '...done.\n'

# test extension

if _test:
    print 'testing hTools2 extension...\n'
    B = ExtensionBundle(name='hTools2', path=extension_path)
    #print dir(B)
    B.validate()
    #B.install()
    print '...done\n.'
