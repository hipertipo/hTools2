# [h] hSettings

# imports

import os
import plistlib

import hTools2

# object

class hSettings:

    '''An object to store information about local settings and preferences.

    When initialized, the :py:class:`hSettings` object does the following:

    1. reads the root folder from :py:attr:`hTools2.ROOT`
    2. finds the settings file in this directory
    3. loads the contents of this file into a dictionary
    4. stores it in :py:attr:`hSettings.hDict`

    .. note :: Maybe it would be better to save this file in ``User/Library/Preferences``?

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

    The full path to the settings file.

    >>> from hTools2.objects import hSettings
    >>> s = hSettings()
    >>> print s.path
    /fonts/hSettings.plist

    .. py:attribute:: hSettings.root

    The path to the local root folder for project files, imported from :py:attr:`hTools2.ROOT`. This is the only hardcoded path in :py:mod:`hTools2`.

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

    def __repr__(self):
        return '<hSettings>'

    @property
    def exists(self):
        '''Check if the settings file exists. Returns a boolean.'''
        return os.path.exists(self.path)

    def read(self):
        '''Read settings from ``.plist`` file into :py:attr:`hSettings.hDict`.'''
        if self.exists:
            self.hDict = plistlib.readPlist(self.path)
        else:
            self.hDict = {}

    def write(self):
        '''Write contents of :py:attr:`hSettings.hDict` to its ``.plist`` file.'''
        if os.path.exists(self.root):
            plistlib.writePlist(self.hDict, self.path)
        else:
            print 'cannot save settings, :py:attr:`hTools2.ROOT` folder does not exist.\n'

    def report(self):
        '''Print all settings data to the console.'''
        if self.exists:
            print 'Saving seetings to %s...' % self.path
            for k in self.hDict.keys():
                print k, self.hDict[k]
            print '...done.\n'
        else:
            print 'The settings file `%s` does not exist.' % self.path
