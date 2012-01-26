# [h] interpolate selected glyphs

'''interpolate selected glyphs into a third font'''

from vanilla import *
from AppKit import NSColor

import hTools2.modules.fontutils
import hTools2.modules.color

reload(hTools2.modules.fontutils)
reload(hTools2.modules.color)

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.color import random_color
#from hTools2.modules.interpol import *

class interpolateGlyphsDialog(object):

    _title = 'interpol'
    _padding = 10
    _padding_top = 8
    _row_height = 25
    _button_height = 30
    _button_2 = 18
    _value_box = 60
    _column_2 = _value_box + (_button_2 * 6) + _button_2 - 6
    _width = 123
    _height = 262

    _all_fonts_names = []
    _factor_x = 0.50
    _factor_y = 0.50
    _proportional = True

    def __init__(self):
        if len(AllFonts()) > 0:
            self._all_fonts = AllFonts()
            for f in self._all_fonts:
                self._all_fonts_names.append(get_full_name(f))
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title,
                        closable=True)
            # master 1
            x = self._padding
            y = self._padding_top
            self.w._f1_font = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        self._all_fonts_names,
                        sizeStyle='small')
            y += self._row_height
            # master 2
            self.w._f2_font = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        self._all_fonts_names,
                        sizeStyle='small')
            y += self._row_height
            # target
            self.w._f3_font = PopUpButton(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        self._all_fonts_names,
                        sizeStyle='small')
            y += self._row_height + self._padding - 3
            #-----------
            # factors x
            #-----------
            # x label
            self.w._factor_x_label = TextBox(
                        (x, y + 2,
                        self._button_2,
                        self._button_2),
                        "x",
                        sizeStyle='small')
            x += self._button_2
            # x value
            self.w._factor_x_value = EditText(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        '%0.2f' % self._factor_x,
                        sizeStyle='small',
                        readOnly=False)
            # x minus 001
            x = self._padding
            y += self._row_height
            self.w._factor_x_minus_001 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_x_minus_001_callback)
            x += self._button_2 - 1
            # x plus 001
            self.w._factor_x_plus_001 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_x_plus_001_callback)
            x += self._button_2 - 1
            # x minus 010
            self.w._factor_x_minus_010 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_x_minus_010_callback)
            x += self._button_2 - 1
            # x plus 010
            self.w._factor_x_plus_010 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_x_plus_010_callback)
            x += self._button_2 - 1
            # x minus 100
            self.w._factor_x_minus_100 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_x_minus_100_callback)
            x += self._button_2 - 1
            # x plus 100
            self.w._factor_x_plus_100 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_x_plus_100_callback)            
            #-----------
            # factors y
            #-----------
            y += self._row_height + 3
            x = self._padding
            # y label
            self.w._factor_y_label = TextBox(
                        (x, y + 2,
                        self._button_2,
                        self._button_2),
                        "y",
                        sizeStyle='small')
            x += self._button_2
            # y value
            self.w._factor_y_value = EditText(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        '%0.2f' % self._factor_y,
                        sizeStyle='small',
                        readOnly=False)
            # y minus 001
            x = self._padding
            y += self._row_height
            self.w._factor_y_minus_001 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_y_minus_001_callback)
            x += self._button_2 - 1
            # y plus 001
            self.w._factor_y_plus_001 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_y_plus_001_callback)
            x += self._button_2 - 1
            # y minus 010
            self.w._factor_y_minus_010 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_y_minus_010_callback)
            x += self._button_2 - 1
            # y plus 010
            self.w._factor_y_plus_010 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_y_plus_010_callback)
            x += self._button_2 - 1
            # y minus 100
            self.w._factor_y_minus_100 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '-',
                        sizeStyle='small',
                        callback=self._factor_y_minus_100_callback)
            x += self._button_2 - 1
            # y plus 010
            self.w._factor_y_plus_100 = SquareButton(
                        (x, y,
                        self._button_2,
                        self._button_2),
                        '+',
                        sizeStyle='small',
                        callback=self._factor_y_plus_100_callback)
            # proporional
            #x += self._button_2 + self._padding
            x = self._padding
            y += self._row_height
            self.w._proportional_checkbox = CheckBox(
                        (x, y,
                        -self._padding,
                        self._button_2),
                        "proportional",
                        value=self._proportional,
                        sizeStyle='small',
                        callback=self._proportional_callback)
            #---------
            # buttons
            #---------
            x = self._padding
            y += self._button_2 + self._padding
            self.w.button_apply = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "interpolate",
                        callback=self.apply_callback,
                        sizeStyle='small')
            # open window
            self.w.open()
        else:
            print 'please open one or more fonts to use this dialog.\n'

    # 0.01

    def _factor_x_plus_001_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) + 0.01
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_plus_001_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) + 0.01
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    def _factor_x_minus_001_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) - 0.01
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_minus_001_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) - 0.01
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # 0.10

    def _factor_x_plus_010_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) + 0.1
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_plus_010_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) + 0.1
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    def _factor_x_minus_010_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) - 0.1
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_minus_010_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) - 0.1
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # 1.00

    def _factor_x_plus_100_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) + 1.0
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_plus_100_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) + 1.0
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    def _factor_x_minus_100_callback(self, sender):
        self._factor_x = float(self.w._factor_x_value.get()) - 1.0
        self.w._factor_x_value.set('%0.2f' % self._factor_x)
        if self._proportional:
            self._factor_y = self._factor_x
            self.w._factor_y_value.set('%0.2f' % self._factor_y)

    def _factor_y_minus_100_callback(self, sender):
        self._factor_y = float(self.w._factor_y_value.get()) - 1.0
        self.w._factor_y_value.set('%0.2f' % self._factor_y)
        if self._proportional:
            self._factor_x = self._factor_y
            self.w._factor_x_value.set('%0.2f' % self._factor_x)

    # proportional

    def _proportional_callback(self, sender):
        self._proportional = self.w._proportional_checkbox.get()

    # interpolate

    def apply_callback(self, sender):
        # get fonts
        f1 = self._all_fonts[self.w._f1_font.get()]
        f2 = self._all_fonts[self.w._f2_font.get()]
        f3 = self._all_fonts[self.w._f3_font.get()]
        # get factors
        x = self._factor_x
        y = self._factor_y
        # print info
        print 'interpolating glyphs...\n'
        boolstring = [False, True]
        print '\tmaster 1: %s' % get_full_name(f1)
        print '\tmaster 2: %s' % get_full_name(f2)
        print '\ttarget: %s' % get_full_name(f3)
        print
        print '\tfactor x: %s' % x
        print '\tfactor y: %s' % y
        print '\tproportional: %s' % boolstring[self._proportional]
        print
        # interpolate glyphs
        for gName in f1.selection:
            # check glyphs
            if f2.has_key(gName):
                f3.newGlyph(gName, clear=True)
                # prepare undo
                f3[gName].prepareUndo('interpolate')
                # interpolate
                print '\tinterpolating glyph %s...' % gName
                f3[gName].interpolate((x, y), f2[gName], f1[gName])
                f3[gName].update()
                # create undo
                f3[gName].performUndo()
            else:
                print '\tfont 2 does not have glyph %s' % gName
        f3.update()
        # done
        print
        print '...done.\n'

# run

interpolateGlyphsDialog()

