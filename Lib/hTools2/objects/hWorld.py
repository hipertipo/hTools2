# [h] hWorld

#-------
# debug
#-------

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hsettings
    reload(hsettings)

    # import hproject
    # reload(hproject)

    import hTools2.modules.sysutils
    reload(hTools2.modules.sysutils)

    # import hTools2.modules.fileutils
    # reload(hTools2.modules.fileutils)

#---------
# imports
#---------

import os

from hsettings import hSettings
# from hproject import hProject

from hTools2.modules.sysutils import _ctx
# from hTools2.modules.fileutils import walk

#---------
# objects
#---------

class hWorld:

    '''An object representing the local fonts folder where all project folders live.'''

    # attributes

    settings = None
    context = None

    # methods

    def __init__(self):
        self.settings = hSettings()
        self.context = _ctx

    def projects(self):
        allFiles = os.listdir(self.settings.root)
        projects = []
        for n in allFiles:
            # hTools2 convention: project folders start with _
            if n[:1] == "_":
                projects.append(n[1:])
        return projects
