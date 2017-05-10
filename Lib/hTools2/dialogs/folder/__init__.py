# dialogs.folder

"""A collection of dialogs to do things to all fonts in a given folder."""

# import

from actions import actionsFolderDialog
from ufo2otf import UFOsToOTFsDialog
from otf2ufo import OTFsToUFOsDialog
from woff2ufo import WOFFsToUFOsDialog

# export

__all__ = [
    'actionsFolderDialog',
    'OTFsToUFOsDialog',
    'UFOsToOTFsDialog',
    'WOFFsToUFOsDialog',
]
