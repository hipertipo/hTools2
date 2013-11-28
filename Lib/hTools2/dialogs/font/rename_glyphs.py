# [h] rename glyphs in font

# imports

from mojo.roboFont import CurrentFont

from vanilla import *
from vanilla.dialogs import getFile

from hTools2.modules.fileutils import read_names_list_from_file
from hTools2.modules.fontutils import rename_glyphs_from_list

# objects

class batchRenameGlyphs(object):

    '''A dialog to batch rename glyphs in a font, based on a list of old- and new names.'''

    _title = 'rename'
    _padding = 10
    _padding_top = 10
    _column_1 = 110
    _row_height = 20
    _button_height = 30
    _height = (_button_height * 2) + (_row_height * 2) + (_padding * 4)
    _width = 123

    def __init__(self):
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title,
                        closable=True)
            x = self._padding
            y = self._padding
            # get names file
            self.w.get_file = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "get file...",
                        callback=self.get_file_callback,
                        sizeStyle="small")
            y += self._button_height + self._padding
            # overwrite glyphs
            self.w._overwrite = CheckBox(
                        (x, y,
                        -self._padding,
                        self._row_height),
                        "overwrite",
                        sizeStyle="small",
                        value=True)
            y += self._row_height
            # mark
            self.w._mark = CheckBox(
                        (x, y,
                        -self._padding,
                        self._row_height),
                        "mark",
                        sizeStyle="small",
                        value=True)
            y += self._row_height + self._padding
            # apply
            self.w.apply_button = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "apply",
                        callback=self.apply_callback,
                        sizeStyle='small')
            # default value for self.list_path
            self.list_path = None
            # open window
            self.w.open()

    # callbacks

    def get_file_callback(self, sender):
        returned_path = getFile()
        if returned_path:
            self.list_path = returned_path[0]

    def apply_callback(self, sender):
        _overwrite = self.w._overwrite.get()
        _mark = self.w._mark.get()
        # the apply button was pressed before getting the list file
        if not self.list_path:
        	print 'please get a names list first.\n'
        	return
        names_list = read_names_list_from_file(self.list_path)
        f = CurrentFont()
        if len(names_list) > 0:
            if f is not None:
                rename_glyphs_from_list(f, names_list, overwrite=_overwrite, mark=_mark)
            # no font open
            else:
                print 'please open a font first.\n'
        # no font open
        else:
            print 'please create a valid names list first.\n'
