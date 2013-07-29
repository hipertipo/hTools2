# [h] dialog to generate otfs from all fonts in folder

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.modules.fileutils
    reload(hTools2.modules.fileutils)

# imports

import os

try:
    from mojo.roboFont import RFont
except:
    from robofab.world import RFont

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2.modules.fileutils import walk

# objects

class generateFolderDialog(object):

    #------------
    # attributes
    #------------

    _title = "generate"
    _padding = 10
    _row_height = 20
    _button_height = 30
    _width = 123
    _height = (_button_height * 3) + (_padding * 6) + (_row_height * 5)

    _ufos_folder = None
    _ufos_folder_message = 'select a folder containing .ufo font sources'

    _otfs_folder = None
    _otfs_folder_message = 'leave empty to generate .ofts in the same folder as .ufos'

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # ufos folder
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "ufos folder...",
                    sizeStyle="small",
                    callback=self.ufos_get_folder_callback)
        y += self._button_height + self._padding
        # otfs folder
        self.w.otfs_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "otfs folder...",
                    sizeStyle="small",
                    callback=self.otfs_get_folder_callback)
        y += self._button_height + self._padding
        # options
        self.w._decompose = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "decompose",
                    sizeStyle="small",
                    value=True)
        y += self._row_height
        self.w._overlaps = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "remove overlap",
                    sizeStyle="small",
                    value=True)
        y += self._row_height
        self.w._autohint = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "ps autohint",
                    sizeStyle="small",
                    value=True)
        y += self._row_height
        self.w._release_mode = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "release mode",
                    sizeStyle="small",
                    value=True)
        y += self._row_height + self._padding
        # progress bar
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    isIndeterminate=True)
        y += self._row_height + self._padding
        # buttons
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "generate",
                    callback=self.button_apply_callback,
                    sizeStyle="small")
        # open window
        self.w.open()

    # callbacks

    def ufos_get_folder_callback(self, sender):
        folder_ufos = getFolder()
        self._ufos_folder = folder_ufos[0]

    def otfs_get_folder_callback(self, sender):
        folder_otfs = getFolder()
        self._otfs_folder = folder_otfs[0]

    def button_apply_callback(self, sender):
        if self._ufos_folder is not None:
            _ufo_paths = walk(self._ufos_folder, 'ufo')
            if len(_ufo_paths) > 0:
                # set otfs folder
                if self._otfs_folder is None:
                    self._otfs_folder = self._ufos_folder
                # get parameters
                _decompose = self.w._decompose.get()
                _overlaps = self.w._overlaps.get()
                _autohint = self.w._autohint.get()
                _release_mode = self.w._release_mode.get()
                # print settings
                boolstring = ("False", "True")
                print 'batch generating .otfs for all fonts in folder...\n'
                print '\tufos folder: %s' % self._ufos_folder
                print '\totfs folder: %s' % self._otfs_folder
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
                    otf_path = os.path.join(self._otfs_folder, otf_file)
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
