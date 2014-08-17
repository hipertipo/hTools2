# [h] ufos -> otfs

# imports

import os

try:
    from mojo.roboFont import RFont

except ImportError:
    from robofab.world import RFont

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2 import hDialog
from hTools2.modules.fileutils import walk
from hTools2.modules.messages import no_font_in_folder

# objects

class UFOsToOTFsDialog(hDialog):

    """A dialog to generate ``.otf`` fonts for all ``.ufos`` in a folder.

    .. image:: imgs/folder/ufos2otfs.png

    """

    # attributes

    ufos_folder = None
    ufos_folder_message = 'select a folder containing .ufo font sources'

    otfs_folder = None
    otfs_folder_message = 'leave empty to generate .ofts in the same folder as .ufos'

    # methods

    def __init__(self):
        # window
        self.title = "ufos2otfs"
        self.height = (self.button_height * 3) + (self.padding_y * 6) + (self.text_height * 4) + self.progress_bar
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        # ufos folder
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "ufos folder...",
                    sizeStyle=self.size_style,
                    callback=self.ufos_get_folder_callback)
        y += (self.button_height + self.padding_y)
        # otfs folder
        self.w.otfs_get_folder_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "otfs folder...",
                    sizeStyle=self.size_style,
                    callback=self.otfs_get_folder_callback)
        y += (self.button_height + self.padding_y) -2
        # options
        self.w._decompose = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "decompose",
                    sizeStyle=self.size_style,
                    value=True)
        y += self.text_height
        self.w._overlaps = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "remove overlap",
                    sizeStyle=self.size_style,
                    value=True)
        y += self.text_height
        self.w._autohint = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "ps autohint",
                    sizeStyle=self.size_style,
                    value=True)
        y += self.text_height
        self.w._release_mode = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "release mode",
                    sizeStyle=self.size_style,
                    value=True)
        y += (self.text_height + self.padding_y)
        # progress bar
        self.w.bar = ProgressBar(
                    (x, y,
                    -self.padding_x,
                    self.progress_bar),
                    isIndeterminate=True,
                    sizeStyle=self.size_style)
        y += (self.progress_bar + self.padding_y)
        # buttons
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "generate",
                    callback=self.button_apply_callback,
                    sizeStyle=self.size_style,)
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
        if self.ufos_folder is not None:
            _ufo_paths = walk(self.ufos_folder, 'ufo')
            if len(_ufo_paths) > 0:
                # set otfs folder
                if self.otfs_folder is None:
                    self.otfs_folder = self.ufos_folder
                # get parameters
                _decompose = self.w._decompose.get()
                _overlaps = self.w._overlaps.get()
                _autohint = self.w._autohint.get()
                _release_mode = self.w._release_mode.get()
                # print settings
                boolstring = ("False", "True")
                print 'batch generating .otfs for all fonts in folder...\n'
                print '\tufos folder: %s' % self.ufos_folder
                print '\totfs folder: %s' % self.otfs_folder
                print '\tdecompose: %s' % boolstring[_decompose]
                print '\tremove overlaps: %s' % boolstring[_overlaps]
                print '\tautohint: %s' % boolstring[_autohint]
                print '\trelease mode: %s' % boolstring[_release_mode]
                print
                # batch generate
                self.w.bar.start()
                for ufo_path in _ufo_paths:
                    print '\tgenerating .otf for %s...' % os.path.split(ufo_path)[1]
                    ufo = RFont(ufo_path, showUI=False)
                    # generate otf
                    otf_file = os.path.splitext(os.path.split(ufo_path)[1])[0] + '.otf'
                    otf_path = os.path.join(self.otfs_folder, otf_file)
                    ufo.generate(otf_path, 'otf',
                                decompose=_decompose,
                                autohint=_autohint,
                                checkOutlines=_overlaps,
                                releaseMode=_release_mode)
                    # close
                    ufo.close()
                    print '\t\totf path: %s' % otf_path
                    print '\t\tgeneration sucessful? %s\n' % os.path.exists(otf_path)
                # done
                self.w.bar.stop()
                print '...done.\n'
        # no font in folder
        else:
            print no_font_in_folder
