# [h] genenerate all open fonts dialog

import os

from vanilla import *
from vanilla.dialogs import getFolder

# from hTools2.modules.fontutils import full_name

def full_name(font):
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name 

class GenerateAllOpenFontsDialog(object):

    _title = "generate .otfs for all open fonts"
    _otfs_folder_default = "/Users/gferreira0/Dropbox/hipertipo/hFonts/_Magnetica/_otfs"

    def __init__(self):
        self.w = FloatingWindow((355, 160), self._title, closable=False)
        # ufos folder
        self.w.otfs_label = TextBox((10, 10, -10, 70), "otfs folder")
        self.w.otfs_get_folder_button = Button((-100, 10, -15, 20), "get folder...", callback=self.otfs_get_folder_callback, sizeStyle="small")
        self.w.otfs_folder_value = EditText((10, 40, -15, 22), text=self._otfs_folder_default, sizeStyle="mini")
        # options
        self.w._overlaps = CheckBox((10, 70, -10, 20), "remove overlaps", value=True)
        self.w._decompose = CheckBox((155, 70, -10, 20), "decompose", value=True)
        self.w._autohint = CheckBox((270, 70, -10, 20), "autohint", value=True)
        # progress bar
        self.w.bar = ProgressBar((10, 100, -10, 16), isIndeterminate=True)
        # apply / close
        self.w.button_close = Button((10, -30, 160, 15), "close", callback=self.button_close_callback)
        self.w.button_apply = Button((185, -30, 160, 15), "apply", callback=self.button_apply_callback)
        self.w.open()

    def otfs_get_folder_callback(self, sender):
        folder_otfs = getFolder()
        self.w.otfs_folder_value.set(folder_otfs[0])

    def button_apply_callback(self, sender):
        _all_fonts = AllFonts()
        if len(_all_fonts) > 0:
            # get settings
            _otfs_folder = self.w.otfs_folder_value.get()
            _decompose = self.w._decompose.get()
            _overlaps = self.w._overlaps.get()
            _autohint = self.w._autohint.get()
            _release_mode = True
            # print settings
            boolstring = ("False", "True")
            print 'generating .otfs for all open fonts...\n'
            print '\totfs folder: %s' % _otfs_folder
            print '\tremove overlaps: %s' % boolstring[_overlaps]
            print '\tdecompose: %s' % boolstring[_decompose]
            print '\tautohint: %s' % boolstring[_autohint]
            print '\trelease mode: %s' % _release_mode
            print
            # batch generate
            self.w.bar.start()
            _undo_name = 'generate all open fonts'
            for font in _all_fonts:          
                if font.path is not None:
                    _font_path = font.path
                    print '\tgenerating .otf for %s...' % os.path.split(full_name(font))[1]
                    # generate otf
                    otf_file = os.path.splitext(os.path.split(font.path)[1])[0] + '.otf'
                    otf_path = os.path.join(_otfs_folder, otf_file)
                    font.generate(otf_path, 'otf', decompose=_decompose, autohint=_autohint, checkOutlines=_overlaps, releaseMode=_release_mode, glyphOrder=[])
                    print '\t\totf path: %s' % otf_path
                    print '\t\tgeneration sucessful? %s\n' % os.path.exists(otf_path)
                # skip unsaved open fonts
                else:
                    print '\tskipping "%s", please save this font to file first.\n' % os.path.split(full_name(font))[1]
            # done all
            self.w.bar.stop()
            print '...done.\n'
        # no font open
        else:
            print 'please open at least one font before running this script.\n'

    def button_close_callback(self, sender):
        self.w.close()

GenerateAllOpenFontsDialog()
