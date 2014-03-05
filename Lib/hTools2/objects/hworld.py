# [h] hWorld

# imports

import os

from hTools2.objects.hsettings import hSettings
from hTools2.modules.sysutils import _ctx

# objects

class hWorld:

    '''An object representing the local fonts folder where all project folders live.'''

    # attributes

    #: A ``hSettings`` object with information about the local system.
    settings = None

    #: The environment in which the current script is running: ``RoboFont``, ``FontLab`` and ``NoneLab``.
    context = None

    # methods

    def __init__(self):
        '''Initiate the ``hWorld`` object.'''
        self.settings = hSettings()
        self.context = _ctx

    def __repr__(self):
        return '<hWorld>'

    def projects(self):
        '''Returns a list of all projects contained in the root fonts folder.'''
        allFiles = os.listdir(self.settings.root)
        projects = []
        for n in allFiles:
            # hTools2 convention: project folders start with _
            if n[:1] == "_":
                projects.append(n[1:])
        return projects
