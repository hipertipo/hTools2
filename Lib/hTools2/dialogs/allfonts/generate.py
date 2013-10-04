# [h] generate all fonts dialog

# import

from mojo.roboFont import AllFonts

import os

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2.modules.fontutils import get_full_name

# dialog

class generateAllFontsDialog(object):

    _title = "generate"
    _padding = 10
    _padding_top = 12
    _row_height = 20
    _button_height = 30
    _width = 123
    _height = (_row_height * 5) + (_button_height * 3) + (_padding_top * 7) - 4

    _otfs_folder = '/'

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        # ufos folder
        x = self._padding
        y = self._padding_top
        self.w._test_install = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "test install",
                    sizeStyle='small',
                    callback=self.test_install_callback)
        y += self._button_height + self._padding_top
        self.w.line_1 = HorizontalLine((0, y, -0, 1))
        y += self._padding_top
        self.w.otfs_get_folder_button = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "otfs folder...",
                    callback=self.otfs_get_folder_callback,
                    sizeStyle="small")
        y += self._button_height + self._padding_top
        # options
        self.w._decompose = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "decompose",
                    value=True,
                    sizeStyle='small')
        y += self._row_height
        self.w._overlaps = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "remove overlap",
                    value=True,
                    sizeStyle='small')
        y += self._row_height
        self.w._autohint = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "ps autohint",
                    value=True,
                    sizeStyle='small')
        y += self._row_height
        self.w._release_mode = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "release mode",
                    value=True,
                    sizeStyle='small')
        # progress bar
        y += self._row_height + self._padding
        self.w.bar = ProgressBar(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    isIndeterminate=True)
        # apply
        y += self._row_height + self._padding
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "generate",
                    callback=self.button_apply_callback,
                    sizeStyle='small')
        # open
        self.w.open()

    def otfs_get_folder_callback(self, sender):
        folder_otfs = getFolder()
        if folder_otfs is not None:
            self._otfs_folder = folder_otfs[0]
            print 'otfs folder: %s' % self._otfs_folder
        else:
            print 'no folder selected.\n'

    def test_install_callback(self, sender):
        _all_fonts = AllFonts()
        if len(_all_fonts) > 0:
            for font in _all_fonts:
                font.testInstall()

    def button_apply_callback(self, sender):
        _all_fonts = AllFonts()
        if len(_all_fonts) > 0:
            # get settings
            _decompose = self.w._decompose.get()
            _overlaps = self.w._overlaps.get()
            _autohint = self.w._autohint.get()
            _release_mode = self.w._release_mode.get()
            # print settings
            boolstring = ("False", "True")
            print 'generating .otfs for all open fonts...\n'
            print '\totfs folder: %s' % self._otfs_folder
            print '\tremove overlaps: %s' % boolstring[_overlaps]
            print '\tdecompose: %s' % boolstring[_decompose]
            print '\tautohint: %s' % boolstring[_autohint]
            print '\trelease mode: %s' % boolstring[_release_mode]
            print
            # batch generate
            self.w.bar.start()
            _undo_name = 'generate all open fonts'
            for font in _all_fonts:
                if font.path is not None:
                    _font_path = font.path
                    print '\tgenerating .otf for %s...' % os.path.split(get_full_name(font))[1]
                    # generate otf
                    otf_file = os.path.splitext(os.path.split(font.path)[1])[0] + '.otf'
                    otf_path = os.path.join(self._otfs_folder, otf_file)
                    font.generate(otf_path, 'otf', decompose=_decompose, autohint=_autohint,
                                checkOutlines=_overlaps, releaseMode=_release_mode, glyphOrder=[])
                    print '\t\totf path: %s' % otf_path
                    print '\t\tgeneration sucessful? %s\n' % os.path.exists(otf_path)
                # skip unsaved open fonts
                else:
                    print '\tskipping "%s", please save this font to file first.\n' % os.path.split(get_full_name(font))[1]
            # done all
            self.w.bar.stop()
            print '...done.\n'
        # no font open
        else:
            print 'please open at least one font before running this script.\n'
