# [h] a simple `SelectFonts()` dialog for RoboScripts

try:
    from mojo.roboFont import CurrentFont, AllFonts, RFont
except:
    from robofab.world import CurrentFont, AllFonts, RFont

from dialogKit import *
from vanilla import *
from vanilla.dialogs import getFolder, getFileOrFolder

from hTools2.modules.fileutils import walk

class SelectFonts(object):

    # attributes

    _padding = 15
    _box_height = 25
    _list_height = 200
    _width = 500
    _help_area = _box_height * 2
    _height = _list_height + (_padding * 5) + (_box_height * 2) + _help_area
    _checkbox_1_width = 110
    _checkbox_2_width = 120
    _checkbox_3_width = 110

    _current_font_checkbox = True
    _open_fonts_checkbox = True
    _folder_fonts_checkbox = False

    _help_text =  '1. Add/remove fonts to the list using the checkboxes.\n'
    _help_text += '2. Select one or more fonts from the list.\n'
    _help_text += '3. Click the OK button to complete the selection.'

    _current_font = None
    _open_fonts = []
    _folder = None
    _folder_font_paths = []
    _folder_fonts = []

    _fonts = []
    _selection = []

    def __init__(self, verbose=False):
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
                    self._help_area),
                    self._help_text,
                    sizeStyle='small')
        # open window
        self.w.open()

    # functions

    def __iter__(self):
        '''return the selected fonts'''
        for selection in self._selection:
            yield self.w._fonts_list[selection]

    def _get_folder(self):
        '''select a folder with .ufo fonts'''
        try:
            self._folder = getFolder()[0] # getFileOrFolder
        # no folder selected
        except TypeError:
            self._folder = None

    def _add_folder_fonts(self):
        '''add all fonts form selected folder to list'''
        if len(self._folder_fonts) > 0:
            for font in self._folder_fonts:
                if font not in self.w._fonts_list:
                    self.w._fonts_list.append(font)
                    print 'font %s added to list' % font
                else:
                    print 'font %s already in list' % font
        else:
            print 'no font in folder.'

    def _get_folder_fonts(self):
        '''collect all .ufo fonts in the selected folder'''
        self._folder_font_paths = walk(self._folder, 'ufo')
        for font_path in self._folder_font_paths:
            font = RFont(font_path, showUI=False)
            if font not in self._folder_fonts:
                self._folder_fonts.append(font)

    # callbacks

    def _current_font_callback(self, sender):
        '''triggered every time the `current font` checkbox is selected'''
        if self._current_font is not None:
            _value = sender.get()
            # add current font to list
            if _value:
                if self._current_font not in self.w._fonts_list:
                    print 'added current font to list'
                    self.w._fonts_list.append(self._current_font)
                # current font already in list
                else:
                    print 'font already in list'
            # remove current font from list
            else:
                print 'removed current font from list'
                if self._current_font in self.w._fonts_list:
                    self.w._fonts_list.remove(self._current_font)
        # no current font
        else:
            print 'no CurrentFont available.\n'

    def _open_fonts_callback(self, sender):
        '''triggered every time the `all open fonts` checkbox is selected'''
        _value = sender.get()
        # add open fonts to list
        if _value:
            for font in self._open_fonts:
                if font not in self.w._fonts_list:
                    self.w._fonts_list.append(font)
                    print 'font %s added to list' % font
                # font already in list
                else:
                    print 'font %s already in list' % font
        # remove fonts from list
        else:
            for font in self._open_fonts:
                if font in self.w._fonts_list:
                    # do not remove current font
                    if font != self._current_font:
                        self.w._fonts_list.remove(font)
                        print 'font %s removed from list' % font
                    else:
                        print 'font %s is the current font' % font
                # font not in list
                else:
                    print 'font %s not in list' % font

    def _folder_fonts_callback(self, sender):
        _value = sender.get()
        # add folder fonts to list
        if _value:
            # get folder
            if self._folder is None:
                print 'getting folder'
                self._get_folder()
            # get fonts in folder
            if self._folder is not None:
                self._get_folder_fonts()
            # no folder selected
            else:
                self.w._fonts_folder_checkbox.set(False)
                print 'no folder selected.'
            # add folder fonts to list
            self._add_folder_fonts()
        # remove folder fonts from list
        else:
            for font in self._folder_fonts:
                if font in self.w._fonts_list:
                    if font != self._current_font:
                        self.w._fonts_list.remove(font)
                        print 'font %s removed from list' % font

    def _get_fonts_folder_callback(self, sender):
        print 'getting fonts from folder...'
        self._get_folder()
        if self._folder is not None:
            self._get_folder_fonts()
            # add folder fonts to list
            if len(self._folder_fonts) > 0:
                self._add_folder_fonts()
            else:
                print 'no font in folder.'
        else:
            print 'no folder selected.'

    def selection_callback(self, sender):
        self._selection = sender.getSelection()

    def apply_callback(self, sender):
        return self.__iter__()

    def cancel_callback(self, sender):
        print 'dialog cancelled.'
        yield None
