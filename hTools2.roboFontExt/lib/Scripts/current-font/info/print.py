# [h] clear font info

'''Print different kinds of font info selectively.'''

# import

from vanilla import *

from hTools2.modules.fontinfo import *
from hTools2.modules.color import random_color

# dialog

class clearFontInfoDialog(object):

    _title = 'font info'
    _padding = 13
    _padding_top = 10
    _row_height = 20
    _button_height = 30
    _button_width =  80
    _width = (_button_width * 2) + (_padding * 2) - 1
    _height = _button_height + (_row_height * 11) + (_padding * 3)

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

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        #---------
        # buttons
        #---------
        x = self._padding
        y = self._padding_top
        self.w._select_all = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "select/deselect all",
                    value=False,
                    sizeStyle='small',
                    callback=self._select_all_callback)
        y += self._row_height + self._padding_top
        # button : print data
        self.w.button_print = SquareButton(
                    (x, y - 4,
                    self._button_width,
                    self._button_height),
                    "print",
                    callback=self.print_callback,
                    sizeStyle='small')
        x += self._button_width - 1
        # button : clear data
        self.w.button_clear = SquareButton(
                    (x, y - 4,
                    self._button_width,
                    self._button_height),
                    "clear",
                    callback=self.clear_callback,
                    sizeStyle='small')
        x += self._button_width - 1
        #------------
        # checkboxes
        #------------
        # identification
        x = self._padding
        y += self._button_height + self._padding_top
        self.w._generic_identification = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "generic identification",
                    value=self._generic_identification,
                    sizeStyle='small')
        y += self._row_height
        # legal
        self.w._generic_legal = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "generic legal",
                    value=self._generic_legal,
                    sizeStyle='small')
        y += self._row_height
        # dimension
        self.w._generic_dimension = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "generic dimension",
                    value = self._generic_dimension,
                    sizeStyle='small')
        y += self._row_height
        # miscellaneous
        self.w._generic_miscellaneous = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "generic miscellaneous",
                    value=self._generic_miscellaneous,
                    sizeStyle='small')
        y += self._row_height
        # opentype head
        self.w._opentype_head = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "OpenType head",
                    value=self._opentype_head,
                    sizeStyle='small')
        y += self._row_height
        # opentype hhea
        self.w._opentype_hhea = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "OpenType hhea",
                    value=self._opentype_hhea,
                    sizeStyle='small')
        y += self._row_height
        # opentype name
        self.w._opentype_name = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "OpenType name",
                    value=self._opentype_name,
                    sizeStyle='small')
        y += self._row_height
        # opentype os2
        self.w._opentype_os2 = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "OpenType OS/2",
                    value=self._opentype_os2,
                    sizeStyle='small')
        y += self._row_height
        # opentype vhea
        self.w._opentype_vhea = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "OpenType vhea",
                    value=self._opentype_vhea,
                    sizeStyle='small')
        y += self._row_height
        # postscript data
        self.w._postscript_data = CheckBox(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "PostScript data",
                    value=self._postscript_data,
                    sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def _select_all_callback(self, sender):
        _value = self.w._select_all.get()
        self.set_values(_value)

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

    def print_callback(self, sender):
        self.get_font()
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

# run

clearFontInfoDialog()
