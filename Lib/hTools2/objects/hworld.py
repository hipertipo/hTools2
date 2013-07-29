# [h] hWorld

# debug

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

# objects

class hWorld:

    '''An object representing the local fonts folder where all project folders live.

    .. py:attribute:: settings

    A :py:class:`hSettings` object with information about the local system.

    >>> from hTools2.objects import hWorld
    >>> w = hWorld()
    >>> print w.settings
    <hTools2.objects.hSettings instance at 0x12ac6b560>
    
    .. py:attribute:: context

    The environment in which the current script is running.

    The possible options are: ``RoboFont``, ``FontLab`` and ``NoneLab``.

    >>> from hTools2.objects import hWorld
    >>> w = hWorld()
    >>> print w.context

    '''

    # attributes

    settings = None
    context = None

    # methods

    def __init__(self):
        '''Initiate the ``hWorld`` object.'''
        self.settings = hSettings()
        self.context = _ctx

    def projects(self):
        '''Returns a list of all projects contained in the root fonts folder.

        According to hTools2 conventions, names of project folders start with an underscore.

        >>> from hTools2.objects import hWorld
        >>> w = hWorld()
        >>> print w.projects()
        ['Elementar', 'EMono', 'Modular', ... , 'Publica']

        '''
        allFiles = os.listdir(self.settings.root)
        projects = []
        for n in allFiles:
            # hTools2 convention: project folders start with _
            if n[:1] == "_":
                projects.append(n[1:])
        return projects

