# dialogs.folder

"""A collection of dialogs to do things to all fonts in a given folder."""

# import

from actions import actionsFolderDialog
from ufos2otfs import UFOsToOTFsDialog
from otfs2ufos import OTFsToUFOsDialog
from woffs2ufos import WOFFsToUFOsDialog

# export

__all__ = [
    'actionsFolderDialog',
    'OTFsToUFOsDialog',
    'UFOsToOTFsDialog',
    'WOFFsToUFOsDialog',
]
