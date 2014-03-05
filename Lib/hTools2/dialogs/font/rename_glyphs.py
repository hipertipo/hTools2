# [h] rename glyphs in font

# imports

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from vanilla import *
from vanilla.dialogs import getFile

from hTools2 import hDialog
from hTools2.modules.fileutils import read_names_list_from_file
from hTools2.modules.fontutils import rename_glyphs_from_list
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class batchRenameGlyphs(hDialog):

    '''A dialog to batch rename glyphs in a font, based on a list of old- and new names.

    .. image:: imgs/font/rename-glyphs.png

    '''

    def __init__(self):
            self.title = 'rename'
            self.column_1 = 110
            self.height = (self.button_height * 2) + (self.text_height * 2) + (self.padding_y * 4)
            self.w = FloatingWindow((self.width, self.height), self.title)
            x = self.padding_x
            y = self.padding_y
            # get names file
            self.w.get_file = SquareButton(
                        (x, y,
                        -self.padding_x,
                        self.button_height),
                        "get file...",
                        callback=self.get_file_callback,
                        sizeStyle=self.size_style)
            y += self.button_height + self.padding_y
            # overwrite glyphs
            self.w._overwrite = CheckBox(
                        (x, y,
                        -self.padding_y,
                        self.text_height),
                        "overwrite",
                        sizeStyle=self.size_style,
                        value=True)
            y += self.text_height
            # mark
            self.w._mark = CheckBox(
                        (x, y,
                        -self.padding_y,
                        self.text_height),
                        "mark",
                        sizeStyle=self.size_style,
                        value=True)
            y += self.text_height + self.padding_y
            # apply
            self.w.apply_button = SquareButton(
                        (x, y,
                        -self.padding_y,
                        self.button_height),
                        "apply",
                        callback=self.apply_callback,
                        sizeStyle=self.size_style)
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
        f = CurrentFont()
        if f is not None:
            names_list = read_names_list_from_file(self.list_path)
            if len(names_list) > 0:
                rename_glyphs_from_list(f, names_list, overwrite=_overwrite, mark=_mark)
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
