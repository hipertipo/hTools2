# [h] hWorld

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hsettings
    reload(hsettings)

    import hTools2.modules.sysutils
    reload(hTools2.modules.sysutils)

# imports

import os

from hsettings import hSettings
from hTools2.modules.sysutils import _ctx

# object

class hWorld:

    '''An object representing the local root folder, where all project folders live.'''

    #------------
    # attributes
    #------------

    # a `hSettings` object with information about the local system
    settings = None

    # the environment in which the current script is running
    # options: `RoboFont` / `FontLab` / `NoneLab`
    context = None

    #---------
    # methods
    #---------

    def __init__(self):
        self.settings = hSettings()
        self.context = _ctx

    def projects(self):
        '''Return a list of all project folders contained in the root folder.'''
        allFiles = os.listdir(self.settings.root)
        projects = []
        for n in allFiles:
            # project folders start with an underscore
            if n[:1] == "_":
                projects.append(n[1:])
        return projects
