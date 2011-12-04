# [h] batch convert .otfs to .ufos dialog

import os

from vanilla import *
from vanilla.dialogs import getFolder

from mojo.roboFont import OpenFont

from hTools2.modules.fileutils import walk

class BatchConvertOTFsToUFOsDialog(object):

    _title = "batch convert all .otfs in folder to .ufos"
    _otfs_folder_default = None
    _otfs_folder_message = 'select a folder containing .otf fonts'
    _ufos_folder_default = None
    _ufos_folder_message = 'leave empty to generate .ufos in the same folder as the .otfs'
    _width = 480
    _height = 200
    _padding = 10

    def __init__(self):
        self.w = FloatingWindow(
                (self._width, self._height),
                self._title,
                closable=False)
        # otfs folder
        self.w.otfs_label = TextBox(
                (self._padding,
                self._padding,
                -self._padding,
                70),
                "folder with .otf fonts")
        self.w.otfs_get_folder_button = Button(
                (-100,
                self._padding,
                -self._padding,
                20),
                "get folder...",
                callback=self.otfs_get_folder_callback,
                sizeStyle="small")
        self.w.otfs_folder_value = EditText(
                (self._padding,
                40,
                -self._padding,
                22),
                text=self._otfs_folder_default,
                sizeStyle="mini",
                placeholder = self._otfs_folder_message)
        # ufos folder
        self.w.ufos_label = TextBox(
                (self._padding,
                75,
                -self._padding,
                70),
                "folder for .ufo fonts")
        self.w.ufos_get_folder_button = Button(
                (-100,
                75,
                -self._padding, 20),
                "get folder...",
                callback=self.ufos_get_folder_callback,
                sizeStyle="small")
        self.w.ufos_folder_value = EditText(
                (self._padding,
                105,
                -self._padding,
                22),
                text=self._ufos_folder_default,
                sizeStyle="mini",
                placeholder = self._ufos_folder_message)
        # progress bar
        self.w.bar = ProgressBar(
                (self._padding,
                -60,
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
        _otfs_folder = self.w.otfs_folder_value.get()
        _ufos_folder = self.w.ufos_folder_value.get()
        if _otfs_folder != None:
            _otfs_paths = walk(_otfs_folder, 'otf')
            if len(_otfs_paths) > 0:
                # set ufos folder
                if _ufos_folder == None:
                    _ufos_folder = _otfs_folder
                # print settings
                boolstring = ("False", "True")
                print 'batch generating .ufos for all .otfs in folder...\n'
                print '\totfs folder: %s' % _otfs_folder
                print '\tufos folder: %s' % _ufos_folder
                print
                # batch convert
                self.w.bar.start()
                for otf_path in _otfs_paths:
                    print '\tsaving .ufo for %s...' % os.path.split(otf_path)[1]
                    otf = OpenFont(otf_path, showUI=True)
                    ufo_file = os.path.splitext(os.path.split(otf_path)[1])[0] + '.ufo'
                    ufo_path = os.path.join(_ufos_folder, ufo_file)
                    otf.save(ufo_path)
                    # close
                    otf.close()
                    print '\t\tufo path: %s' % ufo_path
                    print '\t\tconversion sucessful? %s\n' % os.path.exists(ufo_path)
                # done
                self.w.bar.stop()
                print 
                print '...done.\n'

    def button_close_callback(self, sender):
        self.w.close()

# run 

BatchConvertOTFsToUFOsDialog()

