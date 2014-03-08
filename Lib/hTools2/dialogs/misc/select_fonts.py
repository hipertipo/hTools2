# [h] SelectFonts()

'''a simple `AllFonts()`-compatible `SelectFonts()` dialog for RoboScripts'''

#---------------------------------------------------
# based on idea by David Jonathan Ross (FontBureau)
# thanks to Andy Clymer for vanilla-dialogKit hack
#---------------------------------------------------

# imports

try:
    from mojo.roboFont import CurrentFont, AllFonts, RFont

except:
    from robofab.world import CurrentFont, AllFonts, RFont

from dialogKit import *

from vanilla import *
from vanilla.dialogs import getFolder

from hTools2.modules.fileutils import walk

# objects

class SelectFonts(object):

    '''A dialog to select fonts in different ways.

    .. image:: imgs/misc/select-fonts.png

    .. code-block:: python

        from hTools2.dialogs.misc import SelectFonts

        for font in SelectFonts():
            print font

        >>> <Font Grow D>
        >>> <Font Grow E>
        >>> <Font Grow F>
        >>> <Font Publica 55>
        >>> <Font Publica 95>

    '''

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

    _help_text =  '1. Add/remove fonts to the list using the checkboxes at the top.\n'
    _help_text += '2. Select one or more fonts from the list.\n'
    _help_text += '3. Click on the OK button to complete the selection.'

    _current_font = None
    _open_fonts = []
    _folder = None
    _folder_font_paths = []
    _folder_fonts = []

    _fonts = []
    _selection = []

    _list_titles =   [ 'family', 'style', 'glyphs' ]

    # methods

    def __init__(self, verbose=False):
        self._verbose = verbose
        # get open fonts
        self._get_fonts()
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
        _desc = []
        for i in range(len(self._list_titles)):
            _desc.append( { 'title' : self._list_titles[i] } )

        self.w._fonts_list = List(
                    (x, y,
                    -self._padding,
                    self._list_height),
                    [],
                    columnDescriptions=_desc,
                    selectionCallback=self.selection_callback)
        self._update_list()
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

    def __iter__(self):
        '''return the selected fonts'''
        for selection in self._selection:
            yield self._fonts[selection]

    # functions

    def _get_fonts(self):
        '''get open fonts -- CurrentFont() and AllFonts()'''
        self._current_font = CurrentFont()
        self._open_fonts = AllFonts()

    def _get_folder(self):
        '''select a folder with .ufo fonts'''
        try:
            self._folder = getFolder()[0]
        # no folder selected
        except TypeError:
            self._folder = None

    def _add_folder_fonts(self):
        '''add all folder fonts to list'''
        # add folder fonts
        if len(self._folder_fonts) > 0:
            for font in self._folder_fonts:
                # add font
                if font not in self._fonts:
                    self._fonts.append(font)
                    if self._verbose:
                        print 'font %s added to list' % font
                # font already in list
                else:
                    if self._verbose:
                        print 'font %s already in list' % font
        # no fonts to add
        else:
            if self._verbose:
                print 'no font in folder.'
        # update font list
        self._update_list()

    def _get_folder_fonts(self):
        '''collect all .ufo fonts in the selected folder'''
        # get font paths
        self._folder_font_paths = walk(self._folder, 'ufo')
        # open fonts
        for font_path in self._folder_font_paths:
            font = RFont(font_path, showUI=False)
            if font not in self._folder_fonts:
                self._folder_fonts.append(font)

    # callbacks

    def _current_font_callback(self, sender):
        '''triggered every time the `current font` checkbox is clicked'''
        if self._current_font is not None:
            _value = sender.get()
            # add current font to list
            if _value:
                if self._current_font not in self._fonts:
                    if self._verbose:
                        print 'added current font to list'
                    self._fonts.append(self._current_font)
                # current font already in list
                else:
                    if self._verbose:
                        print 'font already in list'
            # remove current font from list
            else:
                if self._current_font in self._fonts:
                    self._fonts.remove(self._current_font)
                if self._verbose:
                    print 'removed current font from the list'
        # no current font
        else:
            if self._verbose:
                print 'no CurrentFont available.\n'
        # update font list
        self._update_list()

    def _open_fonts_callback(self, sender):
        '''triggered every time the `all open fonts` checkbox is clicked'''
        _value = sender.get()
        # add open fonts to list
        if _value:
            for font in self._open_fonts:
                if font not in self._fonts:
                    self._fonts.append(font)
                    if self._verbose:
                        print 'font %s added to list' % font
                # font already in list
                else:
                    if self._verbose:
                        print 'font %s already in list' % font
        # remove fonts from list
        else:
            for font in self._open_fonts:
                if font in self._fonts:
                    # do not remove current font
                    if font != self._current_font:
                        self._fonts.remove(font)
                        if self._verbose:
                            print 'font %s removed from list' % font
                    else:
                        if self._verbose:
                            print 'font %s is the current font' % font
                # font not in list
                else:
                    if self._verbose:
                        print 'font %s not in list' % font
        # update font list
        self._update_list()

    def _folder_fonts_callback(self, sender):
        '''triggered every time the `from folder` checkbox is clicked'''
        _value = sender.get()
        # add folder fonts to list
        if _value:
            # get folder
            if self._folder is None:
                if self._verbose:
                    print 'getting folder'
                self._get_folder()
            # get fonts in folder
            if self._folder is not None:
                if self._verbose:
                    print 'getting fonts in folder'
                self._get_folder_fonts()
            # no folder selected
            else:
                self.w._fonts_folder_checkbox.set(False)
                if self._verbose:
                    print 'no folder selected.'
            # add folder fonts to list
            self._add_folder_fonts()
        # remove folder fonts from list
        else:
            for font in self._folder_fonts:
                if font in self._fonts:
                    if font != self._current_font:
                        self._fonts.remove(font)
                        if self._verbose:
                            print 'font %s removed from list' % font
            # update font list
            self._update_list()

    def _get_fonts_folder_callback(self, sender):
        '''triggered every time the `get folder` button is clicked'''
        # get folder
        if self._verbose:
            print 'getting fonts from folder...'
        self._get_folder()
        # get fonts from folder
        if self._folder is not None:
            self._get_folder_fonts()
            # add folder fonts to list
            if len(self._folder_fonts) > 0:
                self._add_folder_fonts()
            # no font in folder
            else:
                if self._verbose:
                    print 'there are no font files in the selected folder.'
        # no folder selected
        else:
            if self._verbose:
                print 'no folder selected.'

    def _update_list(self):
        list_1 = [ ]
        list_2 = [ ]
        list_3 = [ ]
        for font in self._fonts:
            list_1.append(font.info.familyName)
            list_2.append(font.info.styleName)
            list_3.append(len(font))
        _list = []
        for i in range(len(list_1)):
            _list.append({
                        self._list_titles[0] : list_1[i],
                        self._list_titles[1] : list_2[i],
                        self._list_titles[2] : list_3[i] })
        self.w._fonts_list.set(_list)

    def selection_callback(self, sender):
        self._selection = sender.getSelection()

    def apply_callback(self, sender):
        return self.__iter__()

    def cancel_callback(self, sender):
        if self._verbose:
            print 'dialog cancelled.'
        yield None

