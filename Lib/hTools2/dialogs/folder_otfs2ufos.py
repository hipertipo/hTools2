# [h] dialog to generate otfs from ufos

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

