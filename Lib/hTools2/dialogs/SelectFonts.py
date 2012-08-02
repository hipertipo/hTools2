# [h] a simple `SelectFonts()` dialog for RoboScripts

class SelectFonts(object):

    _padding = 15
    _box_height = 25
    _list_height = 200
    _width = 500
    _height = _list_height + (_padding * 5) + (_box_height * 3)
    _checkbox_1_width = 110
    _checkbox_2_width = 120
    _checkbox_3_width = 110

    _current_font_checkbox = True
    _open_fonts_checkbox = True
    _folder_fonts_checkbox = False

    _current_font = None
    _open_fonts = []
    _folder = None
    _folder_font_paths = []
    _folder_fonts = []

    _fonts = []
    _selection = []

    def __init__(self):
        # get open fonts
        self._current_font = CurrentFont()
        self._open_fonts = AllFonts()
        # open window
        self.w = ModalDialog((self._width, self._height),
                    title="select fonts",
                    okCallback=self.apply_callback,
                    cancelCallback=self.cancel_callback)
        x = self._padding
        y = self._padding
        # current font
        self.w._current_font_checkbox = CheckBox(
                    (x, y,
                    self._checkbox_1_width,
                    self._box_height),
                    "current font",
                    callback=self._current_font_callback)
        # all open fonts
        x += self._checkbox_1_width
        self.w._open_fonts_checkbox = CheckBox(
                    (x, y,
                    self._checkbox_2_width,
                    self._box_height),
                    "all open fonts",
                    callback=self._open_fonts_callback)
        # fonts from folder
        x += self._checkbox_2_width
        self.w._fonts_folder_checkbox = CheckBox(
                    (x, y,
                    self._checkbox_3_width,
                    self._box_height),
                    "from folder",
                    callback=self._folder_fonts_callback)
        x += self._checkbox_3_width
        self.w._get_folder = Button(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "get folder...",
                    callback=self._get_fonts_folder_callback)
        x = self._padding
        y += (self._box_height + self._padding)
        # font list
        self.w._fonts_list = List(
                    (x, y,
                    -self._padding,
                    self._list_height),
                    self._fonts,
                    selectionCallback=self.selection_callback)
        # help text
        y += (self._list_height + self._padding)
        self.w._help_text = TextBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "Select one or more fonts from the list. Use the checkboxes to add/remove fonts.",
                    sizeStyle='small')
        # open window
        self.w.open()

    def __iter__(self):
        for selection in self._selection:
            yield self.w._fonts_list[selection]

    def _current_font_callback(self, sender):
        _value = sender.get()
        if _value:
            if self._current_font not in self.w._fonts_list:
                print 'added current font to list'
                self.w._fonts_list.append(self._current_font)
            else:
                print 'font already in list'
        else:
            print 'removed current font from list'
            if self._current_font in self.w._fonts_list:
                self.w._fonts_list.remove(self._current_font)

    def _open_fonts_callback(self, sender):
        _value = sender.get()
        if _value:
            for font in self._open_fonts:
                if font not in self.w._fonts_list:
                    self.w._fonts_list.append(font)
                    print 'font %s added to list' % font
                else:
                    print 'font %s already in list' % font
        else:
            for font in self._open_fonts:
                if font in self.w._fonts_list:
                    if font != self._current_font:
                        self.w._fonts_list.remove(font)
                        print 'font %s removed from list' % font
                    else:
                        print 'font %s is the current font' % font
                else:
                    print 'font %s not in list' % font

    def _folder_fonts_callback(self, sender):
        _value = sender.get()
        if _value:
            if self._folder is None:
                print 'get folder'
                self._folder = getFolder()[0]
            # get folder fonts
            if self._folder is not None:
                print self._folder
                self._folder_font_paths = walk(self._folder, 'ufo')
                for font_path in self._folder_font_paths:
                    font = RFont(font_path, showUI=False)
                    if font not in self._folder_fonts:
                        self._folder_fonts.append(font)
            # add folder fonts to list
            for font in self._folder_fonts:
                if font not in self.w._fonts_list:
                    self.w._fonts_list.append(font)
                    print 'font %s added to list' % font
                else:
                    print 'font %s already in list' % font
        else:
            for font in self._folder_fonts:
                if font in self.w._fonts_list:
                    if font != self._current_font:
                        self.w._fonts_list.remove(font)
                        print 'font %s removed from list' % font

    def _get_fonts_folder_callback(self, sender):
        print 'get fonts folder... (not implemented yet)'

    def selection_callback(self, sender):
        self._selection = sender.getSelection()

    def apply_callback(self, sender):
        return self.__iter__()

    def cancel_callback(self, sender):
        print 'dialog cancelled.'
        yield None
