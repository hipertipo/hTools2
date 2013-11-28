# [h] otfs -> ufos

# imports

import os

from mojo.roboFont import OpenFont

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2 import hConstants
from hTools2.modules.fileutils import walk

# objects

class OTFsToUFOsDialog(hConstants):

    '''A dialog to generate ``.ufos`` for all ``.otfs`` in a folder.'''

    # attributes

    otfs_folder = None
    ufos_folder = None

    # methods

    def __init__(self):
        # window
        self.title = "otfs2ufos"
        self.width = 123
        self.height = (self.button_height * 3) + (self.padding_y * 5) + self.progress_bar
        self.w = FloatingWindow((self.width, self.height), self.title)
        # otfs folder
        x = self.padding_x
        y = self.padding_y
        self.w.otfs_get_folder_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "otfs folder...",
                    sizeStyle=self.size_style,
                    callback=self.otfs_get_folder_callback)
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

    def ufos_get_folder_callback(self, sender):
        folder_ufos = getFolder()
        self.ufos_folder = folder_ufos[0]

    def otfs_get_folder_callback(self, sender):
        folder_otfs = getFolder()
        self.otfs_folder = folder_otfs[0]

    def button_apply_callback(self, sender):
        if self.otfs_folder is not None:
            _otfs_paths = walk(self.otfs_folder, 'otf')
            if len(_otfs_paths) > 0:
                # set ufos folder
                if self.ufos_folder is None:
                    self.ufos_folder = self.otfs_folder
                # print settings
                boolstring = ("False", "True")
                print 'batch generating ufos for all otfs in folder...\n'
                print '\totfs folder: %s' % self.otfs_folder
                print '\tufos folder: %s' % self.ufos_folder
                print
                # batch convert
                self.w.bar.start()
                for otf_path in _otfs_paths:
                    print '\tcreating ufo from %s...' % os.path.split(otf_path)[1]
                    otf = OpenFont(otf_path, showUI=True) # does not work without UI
                    ufo_file = os.path.splitext(os.path.split(otf_path)[1])[0] + '.ufo'
                    ufo_path = os.path.join(self.ufos_folder, ufo_file)
                    otf.save(ufo_path)
                    # close
                    otf.close()
                    print '\t\tufo path: %s' % ufo_path
                    print '\t\tconversion sucessful? %s\n' % os.path.exists(ufo_path)
                # done
                self.w.bar.stop()
                print
                print '...done.\n'
