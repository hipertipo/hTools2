# [h] clear font info

"""Print different kinds of font info selectively."""

# import

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontinfo import *
from hTools2.modules.color import random_color
from hTools2.modules.messages import no_font_open

# dialog

class clearFontInfoDialog(hDialog):

    """

    .. image:: imgs/font/print-info.png

    """


    # attributes

    _generic_identification = True
    _generic_legal = True
    _generic_dimension = True
    _generic_miscellaneous = True
    _opentype_head = False
    _opentype_hhea = False
    _opentype_name = True
    _opentype_os2 = False
    _opentype_vhea = False
    _postscript_data = False

    # methods

    def __init__(self):
        self.title = 'font info'
        self.height = (self.button_height * 2) + (self.text_height * 11) + (self.padding_y * 5) - 6
        self.w = FloatingWindow((self.width, self.height), self.title)
        # buttons
        x = self.padding_x
        y = self.padding_y - 3
        self.w._select_all = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "(de)select all",
                    value=False,
                    sizeStyle=self.size_style,
                    callback=self._select_all_callback)
        y += self.text_height + self.padding_y
        # button : print data
        self.w.button_print = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "print",
                    callback=self.print_callback,
                    sizeStyle=self.size_style)
        y += self.button_height + self.padding_y
        # button : clear data
        self.w.button_clear = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "clear",
                    callback=self.clear_callback,
                    sizeStyle=self.size_style)
        # identification
        x = self.padding_x
        y += self.button_height + self.padding_y
        self.w._generic_identification = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "identification",
                    value=self._generic_identification,
                    sizeStyle=self.size_style)
        y += self.text_height
        # legal
        self.w._generic_legal = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "legal",
                    value=self._generic_legal,
                    sizeStyle=self.size_style)
        y += self.text_height
        # dimension
        self.w._generic_dimension = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "dimension",
                    value = self._generic_dimension,
                    sizeStyle=self.size_style)
        y += self.text_height
        # miscellaneous
        self.w._generic_miscellaneous = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "miscellaneous",
                    value=self._generic_miscellaneous,
                    sizeStyle=self.size_style)
        y += self.text_height
        # opentype head
        self.w._opentype_head = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "OT head",
                    value=self._opentype_head,
                    sizeStyle=self.size_style)
        y += self.text_height
        # opentype hhea
        self.w._opentype_hhea = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "OT hhea",
                    value=self._opentype_hhea,
                    sizeStyle=self.size_style)
        y += self.text_height
        # opentype name
        self.w._opentype_name = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "OT name",
                    value=self._opentype_name,
                    sizeStyle=self.size_style)
        y += self.text_height
        # opentype os2
        self.w._opentype_os2 = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "OT OS/2",
                    value=self._opentype_os2,
                    sizeStyle=self.size_style)
        y += self.text_height
        # opentype vhea
        self.w._opentype_vhea = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "OT vhea",
                    value=self._opentype_vhea,
                    sizeStyle=self.size_style)
        y += self.text_height
        # postscript data
        self.w._postscript_data = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "PS data",
                    value=self._postscript_data,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    # callbacks

    def _select_all_callback(self, sender):
        value = self.w._select_all.get()
        self.set_values(value)

    def set_values(self, value):
        self.w._generic_identification.set(value)
        self.w._generic_legal.set(value)
        self.w._generic_dimension.set(value)
        self.w._generic_miscellaneous.set(value)
        self.w._opentype_head.set(value)
        self.w._opentype_hhea.set(value)
        self.w._opentype_name.set(value)
        self.w._opentype_os2.set(value)
        self.w._opentype_vhea.set(value)
        self.w._postscript_data.set(value)

    def get_font(self):
        self.font = CurrentFont()

    def get_values(self):
        self._generic_identification = self.w._generic_identification.get()
        self._generic_legal = self.w._generic_legal.get()
        self._generic_dimension = self.w._generic_dimension.get()
        self._generic_miscellaneous = self.w._generic_miscellaneous.get()
        self._opentype_head = self.w._opentype_head.get()
        self._opentype_hhea = self.w._opentype_hhea.get()
        self._opentype_name = self.w._opentype_name.get()
        self._opentype_os2 = self.w._opentype_os2.get()
        self._opentype_vhea = self.w._opentype_vhea.get()
        self._postscript_data = self.w._postscript_data.get()

    def clear_callback(self, sender):
        self.get_font()
        if self.font is not None:
            self.get_values()
            print 'clearing font info...\n'
            if self._generic_identification:
                print '\tclear generic identification...'
                clear_generic_identification(self.font)
            if self._generic_legal:
                print '\tclear generic legal...'
                clear_generic_legal(self.font)
            if self._generic_dimension:
                print '\tclear generic dimension...'
                clear_generic_dimension(self.font)
            if self._generic_miscellaneous:
                print '\tclear generic miscellaneous...'
                clear_generic_miscellaneous(self.font)
            if self._opentype_head:
                print '\tclear OpenType head...'
                clear_opentype_head(self.font)
            if self._opentype_hhea:
                print '\tclear OpenType hhea...'
                clear_opentype_hhea(self.font)
            if self._opentype_name:
                print '\tclear OpenType name...'
                clear_opentype_name(self.font)
            if self._opentype_os2:
                print '\tclear OpenType OS/2...'
                clear_opentype_os2(self.font)
            if self._opentype_vhea:
                print '\tclear OpenType vhea...'
                clear_opentype_vhea(self.font)
            if self._postscript_data:
                print '\tclear PostScript data...'
                clear_postscript_data(self.font)
            print
            self.font.update()
            print '...done.\n'
        else:
            print no_font_open

    def print_callback(self, sender):
        self.get_font()
        if self.font is not None:
            self.get_values()
            print 'print font info...\n'
            if self._generic_identification:
                print_generic_identification(self.font)
            if self._generic_legal:
                print_generic_legal(self.font)
            if self._generic_dimension:
                print_generic_dimension(self.font)
            if self._generic_miscellaneous:
                print_generic_miscellaneous(self.font)
            if self._opentype_head:
                print_opentype_head(self.font)
            if self._opentype_hhea:
                print_opentype_hhea(self.font)
            if self._opentype_name:
                print_opentype_name(self.font)
            if self._opentype_os2:
                print_opentype_os2(self.font)
            if self._opentype_vhea:
                print_opentype_vhea(self.font)
            if self._postscript_data:
                print_postscript_data(self.font)
            print
            self.font.update()
            print '...done.\n'
        else:
            print no_font_open
