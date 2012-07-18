# [h] hTools2.dialogs.batch_folder

try:
    from mojo.roboFont import *
except:
    from robofab.world import *

import os

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2.modules.fileutils import walk
from hTools2.modules.fontutils import *


class actionsFolderDialog(object):

    #------------
    # attributes
    #------------

    _title = 'actions'
    _row_height = 20
    _button_height = 30
    _padding = 10
    _width = 123
    _height = (_row_height * 8) + (_button_height * 2) + (_padding * 5) + 2

    _round = False
    _decompose = False
    _order = False
    _direction = False
    _overlaps = True
    _extremes = False
    _save = False
    _close = False
    _ufos_folder = None

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # ufos folder
        x = self._padding
        y = self._padding
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "ufos folder...",
                    sizeStyle="small",
                    callback=self.ufos_get_folder_callback)
        # round to integers
        y += self._button_height + self._padding
        self.w.round_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "round points",
                    callback=self.round_callback,
                    value=self._round,
                    sizeStyle='small')
        # decompose
        y += self._row_height
        self.w.decompose_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "decompose",
                    callback=self.decompose_callback,
                    value=self._decompose,
                    sizeStyle='small')
        y += self._row_height
        self.w.order_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto order",
                    callback=self.order_callback,
                    value=self._order,
                    sizeStyle='small')
        y += self._row_height
        self.w.direction_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "auto direction",
                    callback=self.direction_callback,
                    value=self._direction,
                    sizeStyle='small')
        y += self._row_height
        self.w.overlaps_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "remove overlap",
                    callback=self.overlaps_callback,
                    value=self._overlaps,
                    sizeStyle='small')
        y += self._row_height
        self.w.extremes_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "add extremes",
                    callback=self.extremes_callback,
                    value=self._overlaps,
                    sizeStyle='small')
        y += self._row_height
        self.w.save_checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "save .ufo",
                    callback=self.save_callback,
                    value=self._save,
                    sizeStyle='small')
        # progress bar
        y += self._row_height + self._padding
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    isIndeterminate=True)
        # buttons
        y += self._row_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback = self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def ufos_get_folder_callback(self, sender):
        folder_ufos = getFolder()
        self._ufos_folder = folder_ufos[0]

    def clear_callback(self, sender):
        self._clear = sender.get()

    def close_font_callback(self, sender):
        self._close = sender.get()

    def round_callback(self, sender):
        self._round = sender.get()

    def save_callback(self, sender):
        self._save = sender.get()

    def decompose_callback(self, sender):
        self._decompose = sender.get()

    def order_callback(self, sender):
        self._order = sender.get()

    def direction_callback(self, sender):
        self._direction = sender.get()

    def overlaps_callback(self, sender):
        self._overlaps = sender.get()

    def extremes_callback(self, sender):
        self._extremes = sender.get()

    def mark_callback(self, sender):
        self._mark = sender.get()

    # apply callback

    def apply_callback(self, sender):
        ufo_paths = walk(self._ufos_folder, 'ufo')
        if len(ufo_paths) > 0:
            print 'transforming all fonts in folder...\n'
            self.w.bar.start()
            for ufo_path in ufo_paths:
                font = RFont(ufo_path, showUI=False)
                print '\ttransforming %s...' % get_full_name(font)
                if self._round:
                    print '\t\trounding points...'
                    font.round()
                if self._decompose:
                    print '\t\tdecomposing...'
                    decompose(font)
                if self._overlaps:
                    print '\t\tremoving overlaps...'
                    font.removeOverlap()
                if self._order:
                    print '\t\tauto contour order...'
                    auto_contour_order(font)
                if self._direction:
                    print '\t\tauto contour direction...'
                    auto_contour_direction(font)
                if self._extremes:
                    print '\t\tadding extreme points...'
                    add_extremes(font)
                if self._save:
                    print '\t\tsaving font...'
                    font.save()
                print '\t...done.\n'
            self.w.bar.stop()
            print '...done.\n'
        # no font open
        else:
            print 'the selected directory contains no .ufo font.\n'

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
        # ufos folder
        x = self._padding
        y = self._padding
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "ufos folder...",
                    sizeStyle="small",
                    callback=self.ufos_get_folder_callback)
        # otfs folder
        y += self._button_height + self._padding
        self.w.otfs_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "otfs folder...",
                    sizeStyle="small",
                    callback=self.otfs_get_folder_callback)
        # options
        y += self._button_height + self._padding
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
        # progress bar
        y += self._row_height + self._padding
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    isIndeterminate=True)
        # buttons
        y += self._row_height + self._padding
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
                    ufo = RFont(ufo_path, showUI=True)
                    # generate otf
                    otf_file = os.path.splitext(os.path.split(ufo_path)[1])[0] + '.otf'
                    otf_path = os.path.join(self._otfs_folder, otf_file)
                    ufo.generate(otf_path,
                                'otf',
                                decompose=_decompose,
                                autohint=_autohint,
                                checkOutlines=_overlaps,
                                releaseMode=_release_mode,
                                glyphOrder=[])
                    # close
                    ufo.close()
                    print '\t\totf path: %s' % otf_path
                    print '\t\tgeneration sucessful? %s\n' % os.path.exists(otf_path)
                # done
                self.w.bar.stop()
                print '...done.\n'

class OTFsToUFOsDialog(object):

    '''batch generate UFOs for all OTFs in folder'''

    #------------
    # attributes
    #------------

    _title = "otfs2ufos"
    _padding = 10
    _row_height = 20
    _button_height = 30
    _width = 123
    _height = (_button_height * 3) + (_padding * 5) + (_row_height) + 1

    _otfs_folder = None
    _ufos_folder = None

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        # otfs folder
        x = self._padding
        y = self._padding
        self.w.otfs_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "otfs folder...",
                    sizeStyle="small",
                    callback=self.otfs_get_folder_callback)
        # ufos folder
        y += self._button_height + self._padding
        self.w.ufos_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "ufos folder...",
                    sizeStyle="small",
                    callback=self.ufos_get_folder_callback)
        # progress bar
        y += self._button_height + self._padding
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    isIndeterminate=True)
        # buttons
        y += self._row_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
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
        if self._otfs_folder is not None:
            _otfs_paths = walk(self._otfs_folder, 'otf')
            if len(_otfs_paths) > 0:
                # set ufos folder
                if self._ufos_folder is None:
                    self._ufos_folder = self._otfs_folder
                # print settings
                boolstring = ("False", "True")
                print 'batch generating .ufos for all .otfs in folder...\n'
                print '\totfs folder: %s' % self._otfs_folder
                print '\tufos folder: %s' % self._ufos_folder
                print
                # batch convert
                self.w.bar.start()
                for otf_path in _otfs_paths:
                    print '\tsaving .ufo for %s...' % os.path.split(otf_path)[1]
                    otf = OpenFont(otf_path, showUI=True)
                    ufo_file = os.path.splitext(os.path.split(otf_path)[1])[0] + '.ufo'
                    ufo_path = os.path.join(self._ufos_folder, ufo_file)
                    otf.save(ufo_path)
                    # close
                    otf.close()
                    print '\t\tufo path: %s' % ufo_path
                    print '\t\tconversion sucessful? %s\n' % os.path.exists(ufo_path)
                # done
                self.w.bar.stop()
                print
                print '...done.\n'

