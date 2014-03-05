# [h] generate all fonts dialog

# import

try:
    from mojo.roboFont import AllFonts
except ImportError:
    from robofab.world import AllFonts

import os

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name

# dialog

class generateAllFontsDialog(hDialog):

    '''

    .. image:: imgs/all-fonts/generate.png

    '''

    _otfs_folder = '/'

    def __init__(self):
        self.title = "generate"
        self.height = (self.text_height * 5) + (self.button_height * 3) + (self.padding_y * 7)
        self.w = FloatingWindow((self.width, self.height), self.title)
        # ufos folder
        x = self.padding_x
        y = self.padding_y
        self.w._test_install = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "test install",
                    sizeStyle=self.size_style,
                    callback=self.test_install_callback)
        y += self.button_height + self.padding_y
        self.w.line_1 = HorizontalLine((0, y, -0, 1))
        y += self.padding_y
        self.w.otfs_get_folder_button = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "otfs folder...",
                    callback=self.otfs_get_folder_callback,
                    sizeStyle=self.size_style)
        y += self.button_height + self.padding_y
        # options
        self.w._decompose = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "decompose",
                    value=True,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._overlaps = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "remove overlap",
                    value=True,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._autohint = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "ps autohint",
                    value=True,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w._release_mode = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "release mode",
                    value=True,
                    sizeStyle=self.size_style)
        # progress bar
        y += self.text_height + self.padding_y
        self.w.bar = ProgressBar(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    isIndeterminate=True,
                    sizeStyle=self.size_style)
        # apply
        y += self.text_height + self.padding_y
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "generate",
                    callback=self.button_apply_callback,
                    sizeStyle=self.size_style)
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
        all_fonts = AllFonts()
        if len(all_fonts) > 0:
            for font in all_fonts:
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
