# [h] batch genenerate folder dialog

import os

from vanilla import *
from vanilla.dialogs import getFolder

# from hTools2.modules.fileutils import walk

def walk(folder, extension):
	files = []
	names = os.listdir(folder)
	for n in names:
		p = os.path.join(folder, n)
		file_name, file_extension = os.path.splitext(n)
		if file_extension[1:] == extension:
			files.append(p)
	return files

class BatchGenerateFolderDialog(object):

    _title = "batch generate .otfs for all .ufos in folder"
    _ufos_folder_default = "/Users/gferreira0/Dropbox/hipertipo/hFonts/_Magnetica/_ufos"
    _otfs_folder_default = None

    def __init__(self):
        self.w = FloatingWindow((355, 230), self._title, closable=False)
        # ufos folder
        self.w.ufos_label = TextBox((10, 10, -10, 70), "folder with .ufo sources")
        self.w.ufos_get_folder_button = Button((-100, 10, -15, 20), "get folder...", callback=self.ufos_get_folder_callback, sizeStyle="small")
        self.w.ufos_folder_value = EditText((10, 40, -15, 22), text=self._ufos_folder_default, sizeStyle="mini")
        # otfs folder
        self.w.otfs_label = TextBox((10, 80, -10, 70), "folder for .otf fonts")
        self.w.otfs_get_folder_button = Button((-100, 80, -15, 20), "get folder...", callback=self.otfs_get_folder_callback, sizeStyle="small")
        self.w.otfs_folder_value = EditText((10, 110, -15, 22), text=self._otfs_folder_default, sizeStyle="mini")
        # options
        self.w._overlaps = CheckBox((10, 150, -10, 20), "remove overlaps", value=True)
        self.w._decompose = CheckBox((155, 150, -10, 20), "decompose", value=True)
        self.w._autohint = CheckBox((270, 150, -10, 20), "autohint", value=True)
        # apply / close
        self.w.button_close = Button((10, -35, 160, 15), "close", callback=self.button_close_callback)
        self.w.button_apply = Button((185, -35, 160, 15), "apply", callback=self.button_apply_callback)
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

                if _otfs_folder == None:
                    _otfs_folder = _ufos_folder

                _decompose = self.w._decompose.get()
                _overlaps = self.w._overlaps.get()
                _autohint = self.w._autohint.get()

                boolstring = ("False", "True")

                # print settings
                print 'batch generating all fonts in folder...\n'
                print '\tufos folder: %s' % _ufos_folder
                print '\totfs folder: %s' % _otfs_folder
                print '\tremove overlaps: %s' % boolstring[_overlaps]
                print '\tdecompose: %s' % boolstring[_decompose]
                print '\tautohint: %s' % boolstring[_autohint]
                print

                # batch generate
                for ufo_path in _ufo_paths:
                    print '\tgenerating otf for %s...' % os.path.split(ufo_path)[1]
                    ufo = RFont(ufo_path, showUI=False)

                    # remove overlaps
                    if _overlaps:
                        print '\t\tremoving overlaps...'
                        ufo.removeOverlap()

                    # generate otf
                    print '\t\tgenerating otf...'
                    otf_file = os.path.splitext(os.path.split(ufo_path)[1])[0] + '.otf'
                    otf_path = os.path.join(_otfs_folder, otf_file)
                    ufo.generate(otf_path, 'otf', decompose=_decompose, autohint=_autohint, glyphOrder=[])

                    # close
                    ufo.close()
                    print '\t\tdone.\n'

                print '...done.\n'

    def button_close_callback(self, sender):
        self.w.close()

BatchGenerateFolderDialog()

