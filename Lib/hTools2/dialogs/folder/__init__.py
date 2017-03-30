# dialogs.folder

'''Dialogs to do things to all fonts in a given folder.'''

from actions import actionsFolderDialog
from ufo2otf import UFOsToOTFsDialog
from otf2ufo import OTFsToUFOsDialog
from woff2ufo import WOFFsToUFOsDialog

__all__ = [
    'actionsFolderDialog',
    'OTFsToUFOsDialog',
    'UFOsToOTFsDialog',
    'WOFFsToUFOsDialog',
]
