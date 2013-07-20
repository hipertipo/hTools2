# [h] hSettings

# imports

import hTools2
reload(hTools2)

import os
import plistlib

# object

class hSettings:

    '''An object to store information about local settings and preferences.'''

    #------------
    # attributes
    #------------

    # path to the local root folder for project files
    root = hTools2.ROOT

    # name of the settings file
    filename = 'hSettings.plist'

    # a dict with general information about the local installation
    hDict = None

    # full path to the `hSettings.plist` file
    path = None

    #---------
    # methods
    #---------

    def __init__(self):
        self.path = os.path.join(self.root, self.filename)
        self.read()

    def read(self, trim=False):
        '''Read settings from `.plist` file into `self.hDict`.'''
        if os.path.exists(self.path):
            self.hDict = plistlib.readPlist(self.path)
        else:
            self.hDict = {}

    def write(self):
        '''Write contents of `self.hDict` to `.plist` file.'''
        if os.path.exists(self.root):
            plistlib.writePlist(self.hDict, self.path)
        else:
            print 'cannot save hSettings, root folder does not exist.\n'

    def print_(self):
        '''Print all settings items to the console.'''
        for k in self.hDict.keys():
            print k, self.hDict[k]

