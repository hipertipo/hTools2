# [h] woffs -> ufos

# imports

import os

try:
    from mojo.roboFont import OpenFont

except ImportError:
    from robofab.world import OpenFont

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2 import hDialog
from hTools2.modules.fileutils import walk
from hTools2.modules.messages import no_font_in_folder

# objects

class WOFFsToUFOsDialog(hDialog):

    """A dialog to generate ``.ufos`` for all ``.woffs`` in a folder.

    .. image:: imgs/folder/woffs2ufos.png

    """

    # attributes

    otfs_folder = None
    ufos_folder = None

    # methods

    def __init__(self):
        # window
        self.title = "woffs2ufos"
        self.height = (self.button_height * 3) + (self.padding_y * 5) + self.progress_bar
        self.w = FloatingWindow((self.width, self.height), self.title)
        # otfs folder
        x = self.padding_x
        y = self.padding_y
        self.w.woffs_get_folder_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "woffs folder...",
                    sizeStyle=self.size_style,
                    callback=self.woffs_get_folder_callback)
        # ufos folder
        y += (self.button_height + self.padding_y)
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "ufos folder...",
                    sizeStyle=self.size_style,
                    callback=self.ufos_get_folder_callback)
        # progress bar
        y += (self.button_height + self.padding_y)
        self.w.bar = ProgressBar(
                    (x, y,
                    -self.padding_x,
                    self.progress_bar),
                    isIndeterminate=True,
                    sizeStyle=self.size_style)
        # buttons
        y += (self.progress_bar + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "generate",
                    callback=self.button_apply_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def woffs_get_folder_callback(self, sender):
        folder_woffs = getFolder()
        self.woffs_folder = folder_woffs[0]

    def ufos_get_folder_callback(self, sender):
        folder_ufos = getFolder()
        self.ufos_folder = folder_ufos[0]

    def button_apply_callback(self, sender):
        if self.woffs_folder is not None:
            _woffs_paths = walk(self.woffs_folder, 'woff')
            if len(_woffs_paths) > 0:
                # set ufos folder
                if self.ufos_folder is None:
                    self.ufos_folder = self.woffs_folder
                # print settings
                boolstring = ("False", "True")
                print 'batch generating ufos for all woffs in folder...\n'
                print '\twoffs folder: %s' % self.woffs_folder
                print '\tufos folder: %s' % self.ufos_folder
                print
                # batch convert
                self.w.bar.start()
                for woff_path in _woffs_paths:
                    print '\tcreating ufo from %s...' % os.path.split(woff_path)[1]
                    woff = OpenFont(woff_path, showUI=True) # does not work without UI
                    ufo_file = os.path.splitext(os.path.split(woff_path)[1])[0] + '.ufo'
                    ufo_path = os.path.join(self.ufos_folder, ufo_file)
                    woff.save(ufo_path)
                    # close
                    woff.close()
                    print '\t\tufo path: %s' % ufo_path
                    print '\t\tconversion sucessful? %s\n' % os.path.exists(ufo_path)
                # done
                self.w.bar.stop()
                print
                print '...done.\n'
        # no font in folder
        else:
            print no_font_in_folder
