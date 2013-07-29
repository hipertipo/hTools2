# dialogs.folder

'''A collection of dialogs to do things to all fonts in a given folder.'''

import hTools2
reload(hTools2)

# debug

if hTools2.DEBUG:

    import actions
    reload(actions)

    import generate
    reload(generate)

    import otfs2ufos
    reload(otfs2ufos)

# import

from actions import actionsFolderDialog
from generate import generateFolderDialog
from otfs2ufos import OTFsToUFOsDialog

# export

__all__ = [
    'actionsFolderDialog',
    'OTFsToUFOsDialog',
    'generateFolderDialog',
]
