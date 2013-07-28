# [h] hSettings

# imports

import hTools2
reload(hTools2)

import os
import plistlib

# object

class hSettings:

    '''An object to store information about local settings and preferences.

    When initialized, :py:class:`hSettings` reads the root folder for projects from :py:attr:`hTools2.ROOT`, loads the ``hSettings.plist`` file from this directory into a dictionary, and stores it in :py:attr:`hSettings.hDict`.

    .. py:attribute:: hSettings.hDict

    A dictionary containing general information about the local installation.

    Currently, :py:attr:`hDict` contains only a few entries for FTP settings, and an additional custom test folder for .otfs.

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.hDict.keys()
    ['test', 'ftp']
    >>> for k in s.hDict['ftp'].keys():
    >>>     print k, s.hDict['ftp'][k]
    url myserver.com
    folder www/mysite/assets/fonts
    password abcd1234
    login username

    .. py:attribute:: hSettings.path

    The full path to the ``hSettings.plist`` file.

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.path
    /fonts/hSettings.plist

    .. py:attribute:: hSettings.root

    The path to the local root folder for project files, imported from :py:attr:`ROOT`. This is the only hardcoded path in :py:mod:`hTools2`.

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.root
    /fonts

    .. py:attribute:: hSettings.filename

    The name of the settings file. By default, ``hSettings.plist``.

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.filename
    hSettings.plist

    '''

    # attributes

    root = hTools2.ROOT
    filename = 'hSettings.plist'
    hDict = None
    path = None

    # methods

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

