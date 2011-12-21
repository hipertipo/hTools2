# [h] clear font info

from vanilla import *
from AppKit import NSColor

import hTools2.modules.fontinfo
reload(hTools2.modules.fontinfo)

from hTools2.modules.fontinfo import *
from hTools2.modules.color import randomColor

class clearFontInfoDialog(object):

    _title = 'clear font info'
    _width = 220
    _height = 435
    _row_height = 25
    _padding = 15
    _padding_top = 10

    _generic_identification = True
    _generic_legal = True
    _generic_dimension = True
    _generic_miscellaneous = True
    _opentype_head = True
    _opentype_hhea = True
    _opentype_name = True
    _opentype_os2 = True
    _opentype_vhea = True
    _postscript_data = True
    
    def __init__(self):
        self.font = CurrentFont()
        self.w = FloatingWindow(
                (self._width, self._height),
                self._title,
                closable=False)
        # identification
        self.w._generic_identification = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 0),
                -self._padding,
                20),
                "generic identification",
                #callback = self.clear_Callback,
                value=self._generic_identification)
        # legal
        self.w._generic_legal = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 1),
                -self._padding,
                20),
                "generic legal",
                #callback = self.clear_Callback,
                value=self._generic_legal)
        # dimension
        self.w._generic_dimension = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 2),
                -self._padding,
                20),
                "generic dimension",
                value = self._generic_dimension)
        # miscellaneous
        self.w._generic_miscellaneous = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 3),
                -self._padding,
                20),
                "generic miscellaneous",
                value=self._generic_miscellaneous)
        # division 1
        self.w.line_1 = HorizontalLine(
                (self._padding,
                self._padding_top + (self._row_height * 4) + 10,
                -self._padding,
                1))
        # opentype head
        self.w._opentype_head = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 5),
                -self._padding,
                20),
                "OpenType head",
                value=self._opentype_head)
        # opentype hhea
        self.w._opentype_hhea = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 6),
                -self._padding,
                20),
                "OpenType hhea",
                value=self._opentype_hhea)
        # opentype name
        self.w._opentype_name = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 7),
                -self._padding,
                20),
                "OpenType name",
                value=self._opentype_name)
        # opentype os2
        self.w._opentype_os2 = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 8),
                -self._padding,
                20),
                "OpenType OS/2",
                value=self._opentype_os2)
        # opentype vhea
        self.w._opentype_vhea = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 9),
                -self._padding,
                20),
                "OpenType vhea",
                value=self._opentype_vhea)
        # division 2
        self.w.line_2 = HorizontalLine(
                (self._padding,
                self._padding_top + (self._row_height * 10) + 10,
                -self._padding,
                1))
        # postscript data
        self.w._postscript_data = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 11),
                -self._padding,
                20),
                "PostScript data",
                value=self._postscript_data)
        # division 3
        self.w.line_3 = HorizontalLine(
                (self._padding,
                self._padding_top + (self._row_height * 12) + 10,
                -self._padding,
                1))
        # button : print data
        self.w.button_print = Button(
                (self._padding,
                -95,
                -self._padding,
                20),
                "print data",
                callback=self.print_callback)
        # button : clear data
        self.w.button_clear = Button(
                (self._padding,
                -65,
                -self._padding,
                20),
                "clear data",
                callback=self.clear_callback)
        # button : close
        self.w.button_close = Button(
                (self._padding,
                -35,
                -self._padding,
                20),
                "close",
                callback=self.close_callback)
        # open window
        self.w.open()

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
        self.get_values()
        print 'clearing font info...\n'
        if self._generic_identification == True:
            print '\tclear generic identification...'
            clear_generic_identification(self.font)
        if self._generic_legal == True:
            print '\tclear generic legal...'
            clear_generic_legal(self.font)
        if self._generic_dimension == True:
            print '\tclear generic dimension...'
            clear_generic_dimension(self.font)
        if self._generic_miscellaneous == True:
            print '\tclear generic miscellaneous...'
            clear_generic_miscellaneous(self.font)
        if self._opentype_head == True:
            print '\tclear OpenType head...'
            clear_opentype_head(self.font)
        if self._opentype_hhea == True:
            print '\tclear OpenType hhea...'
            clear_opentype_hhea(self.font)
        if self._opentype_name == True:
            print '\tclear OpenType name...'
            clear_opentype_name(self.font)
        if self._opentype_os2 == True:
            print '\tclear OpenType OS/2...'
            clear_opentype_os2(self.font)
        if self._opentype_vhea == True:
            print '\tclear OpenType vhea...'
            clear_openType_vhea(self.font)
        if self._postscript_data == True:
            print '\tclear PostScript data...'
            clear_postscript_data(self.font)
        print
        self.font.update()
        print '...done.\n'

    def print_callback(self, sender):
        self.get_values()
        print 'print font info...\n'
        if self._generic_identification == True:
            print_generic_identification(self.font)
        if self._generic_legal == True:
            print_generic_legal(self.font)
        if self._generic_dimension == True:
            print_generic_dimension(self.font)
        if self._generic_miscellaneous == True:
            print_generic_miscellaneous(self.font)
        if self._opentype_head == True:
            print_opentype_head(self.font)
        if self._opentype_hhea == True:
            print_opentype_hhea(self.font)
        if self._opentype_name == True:
            print_opentype_name(self.font)
        if self._opentype_os2 == True:
            print_opentype_os2(self.font)
        if self._opentype_vhea == True:
            print_openType_vhea(self.font)
        if self._postscript_data == True:
            print_postscript_data(self.font)
        print
        self.font.update()
        print '...done.\n'

    def close_callback(self, sender):
        self.w.close()

# run

clearFontInfoDialog()


