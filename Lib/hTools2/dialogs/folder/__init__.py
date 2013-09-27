# dialogs.folder

'''A collection of dialogs to do things to all fonts in a given folder.'''

import hTools2
reload(hTools2)

# debug

if hTools2.DEBUG:

    import actions
    reload(actions)

    import otfs2ufos
    reload(otfs2ufos)

    import ufos2otfs
    reload(ufos2otfs)

# import

from actions import actionsFolderDialog
from otfs2ufos import OTFsToUFOsDialog
from ufos2otfs import UFOsToOTFsDialog

# export

__all__ = [
    'actionsFolderDialog',
    'OTFsToUFOsDialog',
    'UFOsToOTFsDialog',
]
