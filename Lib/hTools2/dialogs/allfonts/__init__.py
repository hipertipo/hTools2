# dialogs.allfonts

'''A collection of dialogs to do things to all open fonts.'''

import hTools2
reload(hTools2)

# debug

if hTools2.DEBUG:

    import actions
    reload(actions)

    import generate
    reload(generate)

# import

from actions import actionsDialog
from generate import generateAllFontsDialog

# export

__all__ = [
    'actionsDialog',
    'generateAllFontsDialog',
]
