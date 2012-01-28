# [h] batch genenerate .otfs from folder dialog

import os

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2.modules.fileutils import walk

class BatchGenerateFolderDialog(object):

    _title = "batch generate .otfs for all .ufos in folder"
    _ufos_folder_default = None
    _ufos_folder_message = 'select a folder containing .ufo font sources'
    _otfs_folder_default = None
    _otfs_folder_message = 'leave empty to generate .ofts in the same folder as .ufos'
    _width = 480
    _height = 235
    _padding = 10

    def __init__(self):
        self.w = FloatingWindow(
                (self._width, self._height),
                self._title,
                closable=False)
        # ufos folder
        self.w.ufos_label = TextBox(
                (self._padding,
                self._padding,
                -self._padding,
                70),
                "folder with .ufo fonts")
        self.w.ufos_get_folder_button = Button(
                (-100,
                self._padding,
                -self._padding, 20),
                "get folder...",
                callback=self.ufos_get_folder_callback,
                sizeStyle="small")
        self.w.ufos_folder_value = EditText(
                (self._padding,
                40,
                -self._padding,
                22),
                text=self._ufos_folder_default,
                sizeStyle="mini",
                placeholder = self._ufos_folder_message)
        # otfs folder
        self.w.otfs_label = TextBox(
                (self._padding,
                75,
                -self._padding,
                70),
                "folder for .otf fonts")
        self.w.otfs_get_folder_button = Button(
                (-100,
                75, 
                -self._padding,
                20),
                "get folder...",
                callback=self.otfs_get_folder_callback,
                sizeStyle="small")
        self.w.otfs_folder_value = EditText(
                (self._padding,
                105,
                -self._padding,
                22),
                text=self._otfs_folder_default,
                sizeStyle="mini",
                placeholder = self._otfs_folder_message)
        # options
        self.w._overlaps = CheckBox(
                (15,
                140,
                -self._padding,
                20),
                "remove overlaps",
                value=True)
        self.w._decompose = CheckBox(
                (155,
                140,
                -self._padding,
                20),
                "decompose",
                value=True)
        self.w._autohint = CheckBox(
                (265,
                140,
                -self._padding,
                20),
                "autohint",
                value=True)
        self.w._release_mode = CheckBox(
                (355,
                140,
                -self._padding,
                20),
                "release mode",
                value=True)
        # progress bar
        self.w.bar = ProgressBar(
                (self._padding,
                175,
                -self._padding,
                16),
                isIndeterminate=True)
        # buttons
        self.w.button_close = Button(
                (self._padding,
                -30,
                (self._width / 2) - 10,
                15),
                "close",
                callback=self.button_close_callback)
        self.w.button_apply = Button(
                ((self._width / 2) + 10,
                -30,
                -self._padding,
                15),
                "apply",
                callback=self.button_apply_callback)
        # open window
        self.w.open()

    def ufos_get_folder_callback(self, sender):
        folder_ufos = getFolder()
        self.w.ufos_folder_value.set(folder_ufos[0])

    def otfs_get_folder_callback(self, sender):
        folder_otfs = getFolder()
        self.w.otfs_folder_value.set(folder_otfs[0])

    def button_apply_callback(self, sender):
        _ufos_folder = self.w.ufos_folder_value.get()
        _otfs_folder = self.w.otfs_folder_value.get()
        if _ufos_folder != None:
            _ufo_paths = walk(_ufos_folder, 'ufo')
            if len(_ufo_paths) > 0:
                # set otfs folder
                if _otfs_folder == None:
                    _otfs_folder = _ufos_folder
                # get parameters                    
                _decompose = self.w._decompose.get()
                _overlaps = self.w._overlaps.get()
                _autohint = self.w._autohint.get()
                _release_mode = self.w._release_mode.get()
                # print settings
                boolstring = ("False", "True")
                print 'batch generating .otfs for all fonts in folder...\n'
                print '\tufos folder: %s' % _ufos_folder
                print '\totfs folder: %s' % _otfs_folder
                print '\tremove overlaps: %s' % boolstring[_overlaps]
                print '\tdecompose: %s' % boolstring[_decompose]
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
                    otf_path = os.path.join(_otfs_folder, otf_file)
                    ufo.generate(
                            otf_path,
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

    def button_close_callback(self, sender):
        self.w.close()

# run 

BatchGenerateFolderDialog()
